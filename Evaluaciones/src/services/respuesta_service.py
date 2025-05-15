from src.schemas.respuesta import RespuestaAlumno, ResultadoQuiz, ResultadoPregunta
from src.db.mongo import quizzes_collection, preguntas_collection
from src.services.ia_service import generar_feedback_ia
from datetime import datetime
from bson import ObjectId

async def evaluar_respuesta(respuesta_data: RespuestaAlumno) -> ResultadoQuiz:
    quiz = await quizzes_collection.find_one({"_id": ObjectId(respuesta_data.quiz_id)})
    if not quiz:
        raise Exception("Quiz no encontrado")

    preguntas_ids = quiz["preguntas"]
    preguntas_cursor = preguntas_collection.find({"_id": {"$in": [ObjectId(pid) for pid in preguntas_ids]}})
    preguntas = await preguntas_cursor.to_list(length=len(preguntas_ids))

    correctas = 0
    detalle = []

    for i, pregunta in enumerate(preguntas):
        seleccionada = respuesta_data.respuestas[i]
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

    return ResultadoQuiz(
        quiz_id=respuesta_data.quiz_id,
        alumno_id=respuesta_data.alumno_id,
        puntuacion=correctas,
        total=len(preguntas),
        detalle=detalle,
        fecha=datetime.utcnow()
    )
