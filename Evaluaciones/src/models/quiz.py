from datetime import datetime
from bson import ObjectId
from typing import List


def get_quiz_document(
    titulo: str,
    tema: str,
    preguntas: List[ObjectId],
    creado_por: str,  
    fecha_inicio: datetime,
    fecha_fin: datetime,
    curso_id: str,
    estado: str = "programado",
        creado_en: datetime = None
) -> dict:
    return {
        "_id": ObjectId(),
        "titulo": titulo,
        "tema": tema,
        "preguntas": preguntas,
        "creado_por": creado_por,
        "curso_id": curso_id,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "estado": estado,
        "creado_en": creado_en or datetime.now()
    }
