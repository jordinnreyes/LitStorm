from fastapi import APIRouter, HTTPException, Depends
from src.schemas.question import QuestionCreate, QuestionResponse
from src.services.question_service import crear_pregunta
from fastapi import Query
from src.services.ia_service import generar_preguntas_con_ia
from typing import List
from src.models.question import get_question_document
from src.db.mongo import preguntas_collection
from src.services.auth import get_current_user, verificar_curso_existe


router = APIRouter(prefix="/preguntas", tags=["Preguntas"])

#Endpoint para crear una pregunta manualmente
@router.post("/", response_model=dict)
async def crear_una_pregunta(pregunta: QuestionCreate, user=Depends(get_current_user)):
    if user["rol"] != "profesor":
        raise HTTPException(status_code=403, detail="Solo los profesores pueden crear preguntas")

    verificar_curso_existe(pregunta.curso_id)

    pregunta_id = await crear_pregunta(pregunta)
    if not pregunta_id:
        raise HTTPException(status_code=500, detail="No se pudo crear la pregunta.")
    return {"id": pregunta_id}

#Endpoint para generar las preguntas con opciones
@router.post("/generar-con-ia/", response_model=List[QuestionCreate])
async def generar_preguntas_desde_ia(
    tema: str = Query(..., description="Tema sobre el cual generar preguntas"),
    cantidad: int = Query(5, ge=1, le=10)
):
    preguntas = await generar_preguntas_con_ia(tema, cantidad)
    if not preguntas:
        raise HTTPException(status_code=500, detail="Error al generar preguntas.")
    return preguntas

#Endpoint para guardar las preguntas seleccionadas
@router.post("/guardar-seleccionadas/", response_model=List[str])
async def guardar_preguntas_seleccionadas(
    preguntas: List[QuestionCreate],
    user=Depends(get_current_user)
):
    if user["rol"] != "profesor":
        raise HTTPException(status_code=403, detail="Solo los profesores pueden guardar preguntas")

    for pregunta in preguntas:
        verificar_curso_existe(pregunta.curso_id)

    try:
        documentos = [
            get_question_document(
                texto=p.texto,
                opciones=p.opciones,
                respuesta_correcta=p.respuesta_correcta,
                explicacion=p.explicacion,
                tema=p.tema,
                curso_id=p.curso_id
            ) for p in preguntas
        ]
        result = await preguntas_collection.insert_many(documentos)
        return [str(pid) for pid in result.inserted_ids]
    except Exception as e:
        print(f"❌ Error guardando preguntas seleccionadas: {e}")
        raise HTTPException(status_code=500, detail="No se pudieron guardar las preguntas seleccionadas.")

