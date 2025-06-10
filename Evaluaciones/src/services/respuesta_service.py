from src.schemas.respuesta import RespuestaAlumno, ResultadoQuiz, ResultadoPregunta, RespuestaQuizCompleto
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
    print(f"Buscando respuestas para quiz_id: {quiz_id}")
    respuestas_cursor = respuestas_collection.find({"quiz_id": quiz_id})
    print(f"Cursor creado para quiz_id: {quiz_id}")
    respuestas = await respuestas_cursor.to_list(length=None)
    print(f"Respuestas obtenidas para quiz_id: {quiz_id}")
    
    if not respuestas:
        print(f"No se encontraron respuestas para quiz_id: {quiz_id}")
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

async def guardar_respuestas_quiz(respuesta_data: RespuestaQuizCompleto) -> ResultadoQuiz:
    """
    Guarda todas las respuestas de un quiz de una sola vez.
    
    Args:
        respuesta_data: Datos de las respuestas a guardar
        
    Returns:
        ResultadoQuiz con el puntaje y detalles de las respuestas
    """
    try:
        print(f"Datos recibidos: {respuesta_data.dict()}")
        
        # Verificar si el quiz existe
        quiz = await quizzes_collection.find_one({"_id": ObjectId(respuesta_data.quiz_id)})
        if not quiz:
            raise ValueError("Quiz no encontrado")
        
        # Obtener todas las preguntas del quiz
        preguntas_ids = [ObjectId(r.pregunta_id) for r in respuesta_data.respuestas]
        print(f"Buscando preguntas con IDs: {preguntas_ids}")
        
        preguntas = await preguntas_collection.find({"_id": {"$in": preguntas_ids}}).to_list(length=None)
        print(f"Preguntas encontradas: {len(preguntas)}")
        
        if len(preguntas) != len(preguntas_ids):
            raise ValueError(f"Algunas preguntas no existen. Esperadas: {len(preguntas_ids)}, Encontradas: {len(preguntas)}")
        
        # Crear diccionario de preguntas para acceso rápido
        preguntas_dict = {str(p["_id"]): p for p in preguntas}
        print(f"Preguntas en diccionario: {list(preguntas_dict.keys())}")
        
        # Calcular puntuación
        correctas = 0
        detalle = []
        
        for i, respuesta in enumerate(respuesta_data.respuestas):
            print(f"\nProcesando respuesta {i+1}:")
            print(f"- Pregunta ID: {respuesta.pregunta_id}")
            print(f"- Respuesta: {respuesta.respuesta}")
            
            pregunta = preguntas_dict.get(respuesta.pregunta_id)
            if not pregunta:
                print(f"  - Pregunta no encontrada en el diccionario")
                continue
                
            print(f"  - Pregunta encontrada: {pregunta['texto'][:50]}...")
            print(f"  - Opciones: {pregunta.get('opciones', [])}")
            print(f"  - Respuesta correcta: {pregunta.get('respuesta_correcta')}")
            
            es_correcta = pregunta.get("respuesta_correcta") == respuesta.respuesta
            print(f"  - ¿Es correcta? {es_correcta}")
            
            if es_correcta:
                correctas += 1
                
            detalle.append(ResultadoPregunta(
                pregunta_id=respuesta.pregunta_id,
                texto=pregunta["texto"],
                respuesta_usuario=int(respuesta.respuesta),  # Aseguramos que sea entero
                correcta=es_correcta,
                explicacion=pregunta.get("explicacion", ""),
                opciones=pregunta.get("opciones", []),
                respuesta_correcta=int(pregunta.get("respuesta_correcta", -1))  # Aseguramos que sea entero
            ))
        
        # Guardar el resultado
        resultado = ResultadoQuiz(
            quiz_id=respuesta_data.quiz_id,
            alumno_id=respuesta_data.alumno_id,
            puntuacion=correctas,
            total=len(preguntas),
            detalle=detalle,
            fecha=datetime.utcnow()
        )
        
        print("\nResultado a guardar:", resultado.dict())
        
        await respuestas_collection.insert_one(resultado.dict())
        
        return resultado
        
    except Exception as e:
        print(f"Error en guardar_respuestas_quiz: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
