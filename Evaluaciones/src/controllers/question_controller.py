from fastapi import APIRouter, HTTPException
from src.schemas.question import QuestionCreate, QuestionResponse
from src.services.question_service import crear_pregunta
from fastapi import Query
from src.services.ia_service import generar_preguntas_con_ia
from typing import List


router = APIRouter(prefix="/preguntas", tags=["Preguntas"])


@router.post("/", response_model=dict)
async def crear_una_pregunta(pregunta: QuestionCreate):
    pregunta_id = await crear_pregunta(pregunta)
    if not pregunta_id:
        raise HTTPException(status_code=500, detail="No se pudo crear la pregunta.")
    return {"id": pregunta_id}


@router.post("/generar-con-ia/", response_model=List[QuestionCreate])
async def generar_preguntas_desde_ia(
    tema: str = Query(..., description="Tema sobre el cual generar preguntas"),
    cantidad: int = Query(5, ge=1, le=10)
):
    preguntas = await generar_preguntas_con_ia(tema, cantidad)
    if not preguntas:
        raise HTTPException(status_code=500, detail="Error al generar preguntas.")
    return preguntas

