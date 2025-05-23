from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..services.auth import get_current_user
from ..db.database import get_db
from ..services.inscripciones import inscribirse_service, obtener_cursos_inscritos
from ..schemas.inscripcion import InscripcionOut

router = APIRouter()


@router.post("/inscribirse/{codigo}")
def inscribirse(
    codigo: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return inscribirse_service(codigo, user, db)


@router.get("/mis-inscripciones", response_model=list[InscripcionOut])
def listar_cursos_inscritos(db: Session = Depends(get_db), user=Depends(get_current_user)):
    inscripciones = obtener_cursos_inscritos(db, user["id"])
    return inscripciones
