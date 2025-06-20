from fastapi import APIRouter, HTTPException, Depends
from src.schemas.quiz import QuizCreate, QuizResumen
from src.schemas.respuesta import RespuestaEnProgreso
from src.services.quiz_service import (
    crear_quiz, 
    obtener_quiz_para_alumno,
    obtener_quizzes_activos_programados,
    guardar_respuesta_pregunta,
    obtener_preguntas_quiz,
    obtener_respuestas_quiz,
    obtener_temas_quizzes
)
from src.services.auth import get_current_user, verificar_curso_existe
from typing import List, Dict
from bson import ObjectId
from src.db.mongo import quizzes_collection


router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

#Endpoint para que el profesor cree un nuevo quiz con título, tema, preguntas y fechas
@router.post("/", response_model=dict)
async def crear_un_quiz(quiz: QuizCreate, user=Depends(get_current_user)):
    if user["rol"] != "profesor":
        raise HTTPException(status_code=403, detail="Solo los profesores pueden crear quizzes")

    verificar_curso_existe(quiz.curso_id)

    quiz_id = await crear_quiz(quiz, user["id"])
    if not quiz_id:
        raise HTTPException(status_code=500, detail="No se pudo crear el quiz.")
    return {"id": quiz_id}

#Endpoint para que el alumno obtenga la pregunta actual del quiz que está respondiendo
@router.get("/{quiz_id}/pregunta", response_model=Dict)
async def obtener_pregunta_quiz(quiz_id: str, user=Depends(get_current_user)):
    if user["rol"] != "alumno":
        raise HTTPException(status_code=403, detail="Solo los alumnos pueden ver los quizzes")
    
    try:
        quiz = await obtener_quiz_para_alumno(quiz_id, user["id"])
        return quiz
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Endpoint para que el alumno guarde su respuesta a la pregunta actual y avance a la siguiente
@router.post("/{quiz_id}/respuesta", response_model=Dict)
async def guardar_respuesta(
    quiz_id: str, 
    respuesta: RespuestaEnProgreso,
    # user=Depends(get_current_user)
):
    # if user["rol"] != "alumno":
    #     raise HTTPException(status_code=403, detail="Solo los alumnos pueden responder quizzes")
    
    # if user["id"] != respuesta.alumno_id:
    #     raise HTTPException(status_code=403, detail="No puedes responder por otro alumno")

    try:
        progreso = await guardar_respuesta_pregunta(
            quiz_id=quiz_id,
            alumno_id=respuesta.alumno_id,
            pregunta_id=str(respuesta.pregunta_actual),
            respuesta=respuesta.respuesta
        )
        return {
            "progreso": progreso.dict(),
            "siguiente_pregunta": progreso.pregunta_actual + 1 if not progreso.completado else None
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#Endpoint para que el alumno vea los quizzes que están activos o programados en su curso (funciona)
@router.get("/activos-programados/{curso_id}", response_model=List[QuizResumen])
async def listar_quizzes_activos_programados(curso_id: int, user=Depends(get_current_user)):
    if user["rol"] != "alumno":
        raise HTTPException(status_code=403, detail="Solo los alumnos pueden ver los quizzes")
    
    verificar_curso_existe(curso_id)

    quizzes = await obtener_quizzes_activos_programados(curso_id)
    if not quizzes:
        raise HTTPException(status_code=404, detail="No hay quizzes activos o programados para este curso.")

    return quizzes

#Endpoint para obtener todas las preguntas de un quiz
@router.get("/{quiz_id}/preguntas", response_model=List[Dict])
async def obtener_preguntas_quiz_completo(
    quiz_id: str, 
    user=Depends(get_current_user)
):
    try:
        # Primero obtener el quiz para verificar que existe y el usuario tiene acceso
        quiz = await quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz no encontrado")
            
        # Verificar que el usuario esté inscrito en el curso del quiz
        # Esto es un ejemplo, necesitarías implementar la lógica de verificación
        # await verificar_acceso_al_curso(user["id"], quiz["curso_id"])
        
        preguntas = await obtener_preguntas_quiz(quiz_id)
        return preguntas
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error obteniendo preguntas del quiz: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener las preguntas del quiz")

#Endpoint para obtener respuestas de un quiz
@router.get("/{quiz_id}/respuestas", response_model=Dict)
async def ver_respuestas_quiz(quiz_id: str):
    """
    Obtiene todas las respuestas de un quiz.
    No requiere autenticación y muestra todas las respuestas.
    """
    try:
        respuestas = await obtener_respuestas_quiz(quiz_id)
        return respuestas
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error obteniendo respuestas: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener las respuestas del quiz")


@router.get("/temas/", response_model=List[str])
async def listar_temas_quizzes():
    """
    Obtiene una lista de todos los temas únicos de los quizzes existentes.
    Útil para mostrar un listado de temas disponibles al crear o filtrar quizzes.
    """
    try:
        return await obtener_temas_quizzes()
    except Exception as e:
        print(f"Error listando temas: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener la lista de temas")






# Endpoint para que el profesor obtenga todos los quizzes de un curso (sin filtrar por estado)
@router.get("/por_curso/{curso_id}", response_model=List[QuizResumen])
async def obtener_quizzes_por_curso(curso_id: int, user=Depends(get_current_user)):
    if user["rol"] != "profesor":
        raise HTTPException(status_code=403, detail="Solo los profesores pueden ver los quizzes de un curso")
    
    verificar_curso_existe(curso_id)

    quizzes_cursor = quizzes_collection.find({"curso_id": curso_id})
    quizzes = await quizzes_cursor.to_list(length=None)

    return [
        QuizResumen(
            id=str(q["_id"]),
            titulo=q["titulo"],
            tema=q["tema"],
            fecha_inicio=q["fecha_inicio"],
            fecha_fin=q["fecha_fin"],
            estado=q["estado"]
        ) for q in quizzes
    ]
