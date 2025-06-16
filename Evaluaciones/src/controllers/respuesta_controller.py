from fastapi import APIRouter, HTTPException, Depends
from src.schemas.respuesta import RespuestaAlumno, ResultadoQuiz, RespuestaQuizCompleto
from src.services.respuesta_service import evaluar_respuesta, obtener_estadisticas_quiz, guardar_respuestas_quiz, obtener_respuestas_quiz_por_alumno
from src.services.auth import get_current_user
from typing import Dict
from src.db.mongo import respuestas_collection


router = APIRouter(prefix="/respuestas", tags=["Respuestas"])

#Endpoint para evaluar todas las respuestas del alumno al finalizar el quiz y mostrar resultados
@router.post("/evaluar", response_model=ResultadoQuiz)
async def responder_quiz(respuesta: RespuestaQuizCompleto):
    try:
        print("📥 Recibido en backend:", respuesta)
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





@router.get("/verificar/{quiz_id}/{alumno_id}")
async def verificar_respuesta(quiz_id: str, alumno_id: str):
    try:
        print("🔍 Buscando en Mongo:", {"quiz_id": quiz_id, "alumno_id": alumno_id})

        respuesta = await respuestas_collection.find_one({
            "quiz_id": quiz_id,
            "alumno_id": alumno_id  # 👈 sin cast a int
        })
        return {"respondido": bool(respuesta)}
    except Exception as e:
        print("Error verificando respuesta:", e)
        return {"respondido": False}


@router.get("/respuestas/{quiz_id}/{alumno_id}", response_model=Dict)
async def ver_respuestas_de_alumno(quiz_id: str, alumno_id: str):
    """
    Devuelve las respuestas de un quiz específico para un alumno.
    """
    try:
        return await obtener_respuestas_quiz_por_alumno(quiz_id, alumno_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener respuestas del alumno")
