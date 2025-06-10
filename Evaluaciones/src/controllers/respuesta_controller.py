from fastapi import APIRouter, HTTPException, Depends
from src.schemas.respuesta import RespuestaAlumno, ResultadoQuiz, RespuestaQuizCompleto
from src.services.respuesta_service import evaluar_respuesta, obtener_estadisticas_quiz, guardar_respuestas_quiz
from src.services.auth import get_current_user
from typing import Dict

router = APIRouter(prefix="/respuestas", tags=["Respuestas"])

#Endpoint para evaluar todas las respuestas del alumno al finalizar el quiz y mostrar resultados
@router.post("/evaluar", response_model=ResultadoQuiz)
async def responder_quiz(respuesta: RespuestaAlumno):
    try:
        resultado = await evaluar_respuesta(respuesta)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Endpoint para que el profesor vea las estadísticas de un quiz específico
@router.get("/{quiz_id}/estadisticas", response_model=Dict)
async def obtener_estadisticas(quiz_id: str, user=Depends(get_current_user)):
    # if user["rol"] != "profesor":
    #     raise HTTPException(status_code=403, detail="Solo los profesores pueden ver las estadísticas")
    
    try:
        estadisticas = await obtener_estadisticas_quiz(quiz_id)
        return estadisticas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/completar-quiz/", response_model=ResultadoQuiz)
async def completar_quiz(respuesta_data: RespuestaQuizCompleto):
    try:
        return await guardar_respuestas_quiz(respuesta_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error guardando respuestas: {e}")
        raise HTTPException(status_code=500, detail="Error al guardar las respuestas")