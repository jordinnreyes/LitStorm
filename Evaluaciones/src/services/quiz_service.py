from bson import ObjectId
from ..models.quiz import get_quiz_document
from ..db.mongo import quizzes_collection
from ..schemas.quiz import QuizCreate
from typing import Optional, List
from datetime import datetime
from ..utils.estado_quiz import determinar_estado

async def crear_quiz(quiz_data: QuizCreate, creado_por: str) -> Optional[str]:
    try:
        preguntas_ids = [ObjectId(pid) for pid in quiz_data.preguntas]

        quiz_doc = get_quiz_document(
            titulo=quiz_data.titulo,
            tema=quiz_data.tema,
            preguntas=preguntas_ids,
            creado_por=creado_por,
            curso_id=quiz_data.curso_id,
            fecha_inicio=quiz_data.fecha_inicio,
            fecha_fin=quiz_data.fecha_fin,
            estado=quiz_data.estado
        )

        result = await quizzes_collection.insert_one(quiz_doc)
        return str(result.inserted_id)
    
    except Exception as e:
        print(f"Error creando quiz: {e}")
        return None


async def obtener_quizzes_activos_por_curso(curso_id: str) -> List[dict]:
    ahora = datetime.now()

    cursor = quizzes_collection.find({
        "curso_id": curso_id,
        "fecha_inicio": {"$lte": ahora},
        "fecha_fin": {"$gte": ahora}
    })

    quizzes = []
    async for quiz in cursor:
        estado_actual = determinar_estado(quiz["fecha_inicio"], quiz["fecha_fin"])
        if estado_actual == "activo":
            quizzes.append({
                "id": str(quiz["_id"]),
                "titulo": quiz["titulo"],
                "tema": quiz["tema"],
                "fecha_inicio": quiz["fecha_inicio"],
                "fecha_fin": quiz["fecha_fin"],
                "estado": estado_actual
            })

    return quizzes