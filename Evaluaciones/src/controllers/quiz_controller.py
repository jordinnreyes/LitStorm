from fastapi import APIRouter, HTTPException
from src.schemas.quiz import QuizCreate
from src.services.quiz_service import crear_quiz

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


@router.post("/", response_model=dict)
async def crear_un_quiz(quiz: QuizCreate):
    quiz_id = await crear_quiz(quiz)
    if not quiz_id:
        raise HTTPException(status_code=500, detail="No se pudo crear el quiz.")
    return {"id": quiz_id}
