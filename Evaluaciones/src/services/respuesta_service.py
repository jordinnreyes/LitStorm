from src.schemas.respuesta import RespuestaAlumno, ResultadoQuiz, ResultadoPregunta
from src.db.mongo import quizzes_collection, preguntas_collection, respuestas_collection
from src.services.ia_service import generar_feedback_ia
from datetime import datetime
from bson import ObjectId
from typing import List, Dict

#Evalua la respuesta
async def evaluar_respuesta(respuesta_data: RespuestaAlumno) -> ResultadoQuiz:
    # Verificar si el quiz existe y está activo
    quiz = await quizzes_collection.find_one({"_id": ObjectId(respuesta_data.quiz_id)})
    if not quiz:
        raise ValueError("Quiz no encontrado")

    # Verificar si el quiz está activo
    ahora = datetime.now()
    if ahora < quiz["fecha_inicio"]:
        raise ValueError("El quiz aún no ha comenzado")
    if ahora > quiz["fecha_fin"]:
        raise ValueError("El quiz ya ha terminado")

    # Verificar si el alumno ya respondió este quiz
    respuesta_previa = await respuestas_collection.find_one({
        "quiz_id": respuesta_data.quiz_id,
        "alumno_id": respuesta_data.alumno_id
    })
    if respuesta_previa:
        raise ValueError("Ya has respondido este quiz anteriormente")

    preguntas_ids = quiz["preguntas"]
    preguntas_cursor = preguntas_collection.find({"_id": {"$in": preguntas_ids}})
    preguntas = await preguntas_cursor.to_list(length=len(preguntas_ids))

    if len(respuesta_data.respuestas) != len(preguntas):
        raise ValueError(f"El número de respuestas ({len(respuesta_data.respuestas)}) no coincide con el número de preguntas ({len(preguntas)})")

    correctas = 0
    detalle = []

    for i, pregunta in enumerate(preguntas):
        seleccionada = respuesta_data.respuestas[i]
        if seleccionada < 0 or seleccionada >= len(pregunta["opciones"]):
            raise ValueError(f"Respuesta inválida para la pregunta {i + 1}")

        es_correcta = seleccionada == pregunta["respuesta_correcta"]
        if es_correcta:
            correctas += 1

        feedback_ia = None
        if not es_correcta:
            feedback_ia = await generar_feedback_ia(
                pregunta["texto"],
                pregunta["opciones"],
                pregunta["respuesta_correcta"],
                seleccionada
            )

        detalle.append(ResultadoPregunta(
            texto=pregunta["texto"],
            correcta=es_correcta,
            respuesta_usuario=pregunta["opciones"][seleccionada],
            respuesta_correcta=pregunta["opciones"][pregunta["respuesta_correcta"]],
            explicacion=pregunta["explicacion"],
            feedback_ia=feedback_ia
        ))

    resultado = ResultadoQuiz(
        quiz_id=respuesta_data.quiz_id,
        alumno_id=respuesta_data.alumno_id,
        puntuacion=correctas,
        total=len(preguntas),
        detalle=detalle,
        fecha=datetime.utcnow()
    )

    await respuestas_collection.insert_one(resultado.dict())

    return resultado

#Esto es para la profesora, da una estadistica por cada quiz resuelto 
async def obtener_estadisticas_quiz(quiz_id: str) -> Dict:
    # Obtener todas las respuestas para este quiz
    respuestas_cursor = respuestas_collection.find({"quiz_id": quiz_id})
    respuestas = await respuestas_cursor.to_list(length=None)
    
    if not respuestas:
        return {
            "total_alumnos": 0,
            "promedio_puntuacion": 0,
            "preguntas_problematicas": []
        }

    # Calcular estadísticas básicas
    total_alumnos = len(respuestas)
    promedio_puntuacion = sum(r["puntuacion"] for r in respuestas) / total_alumnos

    # Analizar preguntas problemáticas
    errores_por_pregunta = {}
    for respuesta in respuestas:
        for i, detalle in enumerate(respuesta["detalle"]):
            if not detalle["correcta"]:
                if i not in errores_por_pregunta:
                    errores_por_pregunta[i] = {
                        "texto": detalle["texto"],
                        "count": 0
                    }
                errores_por_pregunta[i]["count"] += 1

    # Ordenar preguntas por número de errores
    preguntas_problematicas = sorted(
        [{"pregunta": info["texto"], "total_errores": info["count"]} 
         for info in errores_por_pregunta.values()],
        key=lambda x: x["total_errores"],
        reverse=True
    )

    return {
        "total_alumnos": total_alumnos,
        "promedio_puntuacion": round(promedio_puntuacion, 2),
        "preguntas_problematicas": preguntas_problematicas[:3]  # Top 3 preguntas más problemáticas
    }
