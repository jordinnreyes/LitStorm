from src.models.question import get_question_document
from src.schemas.question import QuestionCreate
from src.db.mongo import preguntas_collection
from typing import Optional
from bson import ObjectId


async def crear_pregunta(pregunta_data: QuestionCreate) -> Optional[str]:
    try:
        pregunta_doc = get_question_document(
            texto=pregunta_data.texto,
            opciones=pregunta_data.opciones,
            respuesta_correcta=pregunta_data.respuesta_correcta,
            explicacion=pregunta_data.explicacion,
            tema=pregunta_data.tema
        )

        result = await preguntas_collection.insert_one(pregunta_doc)
        return str(result.inserted_id)

    except Exception as e:
        print(f"Error creando pregunta: {e}")
        return None
