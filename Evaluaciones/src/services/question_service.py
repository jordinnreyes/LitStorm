from src.models.question import get_question_document
from src.schemas.question import QuestionCreate, QuestionResponse
from src.db.mongo import preguntas_collection
from typing import List, Optional
from bson import ObjectId


async def crear_pregunta(pregunta_data: QuestionCreate) -> Optional[str]:
    try:
        pregunta_doc = get_question_document(
            texto=pregunta_data.texto,
            opciones=pregunta_data.opciones,
            respuesta_correcta=pregunta_data.respuesta_correcta,
            explicacion=pregunta_data.explicacion,
            tema=pregunta_data.tema,
            curso_id=pregunta_data.curso_id
        )

        result = await preguntas_collection.insert_one(pregunta_doc)
        return str(result.inserted_id)

    except Exception as e:
        print(f"Error creando pregunta: {e}")
        return None


async def obtener_todas_las_preguntas() -> List[QuestionResponse]:
    """
    Obtiene todas las preguntas de la base de datos sin filtros.
    
    Returns:
        List[QuestionResponse]: Lista de todas las preguntas
    """
    try:
        cursor = preguntas_collection.find()
        preguntas = []
        async for doc in cursor:
            preguntas.append(QuestionResponse(
                id=str(doc["_id"]),
                texto=doc["texto"],
                opciones=doc["opciones"],
                respuesta_correcta=doc["respuesta_correcta"],
                explicacion=doc.get("explicacion", ""),
                tema=doc.get("tema", ""),
                curso_id=str(doc.get("curso_id", "")),
                creado_en=doc.get("creado_en", "")
            ))
        return preguntas
    except Exception as e:
        print(f"Error obteniendo todas las preguntas: {e}")
        raise Exception("Error interno al obtener las preguntas")


async def obtener_preguntas_por_tema(tema: str) -> List[QuestionResponse]:
    try:
        print(f"Tema proporcionado: '{tema.strip()}'")
        regex = tema.strip()
        cursor = preguntas_collection.find({"tema": {"$regex": regex, "$options": "i"}})
        
        preguntas = []
        async for doc in cursor:
            print(f"Tema en documento: '{doc.get('tema', '')}'")
            preguntas.append(QuestionResponse(
                id=str(doc["_id"]),
                texto=doc["texto"],
                opciones=doc["opciones"],
                respuesta_correcta=doc["respuesta_correcta"],
                explicacion=doc.get("explicacion", ""),
                tema=doc.get("tema", ""),
                curso_id=str(doc.get("curso_id", "")),
                creado_en=doc.get("creado_en", None)
            ))
            
        return preguntas
        
    except Exception as e:
        print(f"Error obteniendo preguntas por tema: {e}")
        raise Exception("Error interno al obtener preguntas por tema")
