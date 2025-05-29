from datetime import datetime
from bson import ObjectId


def get_question_document(
    texto: str,
    opciones: list[str],
    respuesta_correcta: int,
    explicacion: str,
    tema: str,
    curso_id: str,  # nuevo
    creado_en: datetime = None
) -> dict:
    return {
        "_id": ObjectId(),
        "texto": texto,
        "opciones": opciones,
        "respuesta_correcta": respuesta_correcta,
        "explicacion": explicacion,
        "tema": tema,
        "curso_id": curso_id,
        "creado_en": creado_en or datetime.now()
    }
