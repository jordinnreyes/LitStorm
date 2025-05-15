from fastapi import APIRouter, HTTPException
from src.schemas.respuesta import RespuestaAlumno, ResultadoQuiz
from src.services.respuesta_service import evaluar_respuesta

router = APIRouter(prefix="/respuestas", tags=["Respuestas"])

@router.post("/evaluar", response_model=ResultadoQuiz)
async def responder_quiz(respuesta: RespuestaAlumno):
    try:
        resultado = await evaluar_respuesta(respuesta)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
