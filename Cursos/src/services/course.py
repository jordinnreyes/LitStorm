import random
import string
from sqlalchemy.orm import Session
from src.models.course import Course
from src.models.inscripcion import Inscripcion
from fastapi import HTTPException


def generar_codigo_acceso(longitud=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=longitud))


def crear_curso_service(curso_data, user, db: Session):
    if user["rol"] not in ("profesor", "admin"):
        raise HTTPException(status_code=403, detail="No autorizado")

    codigo = generar_codigo_acceso()
    nuevo = Course(
        **curso_data.model_dump(),
        profesor_id=user["id"],
        codigo_acceso=codigo
    )

    db.add(nuevo)
    db.flush()  

    inscripcion = Inscripcion(user_id=user["id"], curso_id=nuevo.id)
    db.add(inscripcion)

    db.commit()
    db.refresh(nuevo)
    return nuevo