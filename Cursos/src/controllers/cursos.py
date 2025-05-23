from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.course import Course
from ..schemas.course import CursoBase, CursoOut
from ..services.auth import get_current_user
from ..db.database import get_db
from ..services.course import crear_curso_service


router = APIRouter()

@router.post("/", response_model=CursoOut)
def crear_curso(
    curso: CursoBase,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return crear_curso_service(curso, user, db)

@router.get("/", response_model=list[CursoOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Course).all()
