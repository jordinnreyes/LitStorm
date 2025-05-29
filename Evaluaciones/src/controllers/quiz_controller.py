from fastapi import APIRouter, HTTPException, Depends
from src.schemas.quiz import QuizCreate, QuizResumen
from src.services.quiz_service import crear_quiz, obtener_quizzes_activos_por_curso
from src.services.auth import get_current_user, verificar_curso_existe
from typing import List


router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

#Crea un quiz
@router.post("/", response_model=dict)
async def crear_un_quiz(quiz: QuizCreate, user=Depends(get_current_user)):
    if user["rol"] != "profesor":
        raise HTTPException(status_code=403, detail="Solo los profesores pueden crear quizzes")

    verificar_curso_existe(quiz.curso_id)

    quiz_id = await crear_quiz(quiz, user["id"])
    if not quiz_id:
        raise HTTPException(status_code=500, detail="No se pudo crear el quiz.")
    return {"id": quiz_id}

#controller para listar los quizzes por curso
@router.get("/activos/{curso_id}", response_model=List[QuizResumen])
async def listar_quizzes_activos_por_curso(curso_id: str):
    verificar_curso_existe(curso_id)

    quizzes = await obtener_quizzes_activos_por_curso(curso_id)
    if not quizzes:
        raise HTTPException(status_code=404, detail="No hay quizzes activos para este curso.")

    return quizzes