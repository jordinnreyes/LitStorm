from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import SessionLocal
from ..models.inscripcion import Inscripcion
from ..schemas.inscripcion import InscripcionIn
from ..services.auth import get_current_user
from ..db.database import get_db

router = APIRouter()

@router.post("/")
def inscribirse(ins: InscripcionIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user["rol"] != "alumno":
        raise HTTPException(status_code=403, detail="Solo alumnos pueden inscribirse")
    
    ya_inscrito = db.query(Inscripcion).filter_by(user_id=user["id"], curso_id=ins.curso_id).first()
    if ya_inscrito:
        raise HTTPException(status_code=400, detail="Ya estás inscrito en este curso")

    nueva = Inscripcion(user_id=user["id"], curso_id=ins.curso_id)
    db.add(nueva)
    db.commit()
    return {"mensaje": "Inscripción exitosa"}
