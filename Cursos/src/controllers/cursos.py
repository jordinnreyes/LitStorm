from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.course import Course
from ..schemas.course import CursoBase, CursoOut
from ..services.auth import get_current_user
from ..db.database import get_db


router = APIRouter()

@router.post("/", response_model=CursoOut)
def crear_curso(curso: CursoBase, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user["rol"] not in ("profesor", "admin"):
        raise HTTPException(status_code=403, detail="No autorizado")
    nuevo = Course(**curso.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[CursoOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Course).all()
