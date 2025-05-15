from bson import ObjectId
from src.models.quiz import get_quiz_document
from src.db.mongo import quizzes_collection
from src.schemas.quiz import QuizCreate
from typing import Optional


async def crear_quiz(quiz_data: QuizCreate) -> Optional[str]:
    try:
        preguntas_ids = [ObjectId(pid) for pid in quiz_data.preguntas]

        quiz_doc = get_quiz_document(
            titulo=quiz_data.titulo,
            tema=quiz_data.tema,
            preguntas=preguntas_ids,
            creado_por=quiz_data.creado_por,
            fecha_inicio=quiz_data.fecha_inicio,
            fecha_fin=quiz_data.fecha_fin,
            estado=quiz_data.estado
        )

        result = await quizzes_collection.insert_one(quiz_doc)
        return str(result.inserted_id)
    
    except Exception as e:
        print(f"Error creando quiz: {e}")
        return None
