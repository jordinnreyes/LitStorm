from sqlalchemy.orm import Session
from src.models.course import Course
from src.models.inscripcion import Inscripcion
from fastapi import HTTPException

def inscribirse_service(codigo: str, user, db: Session):
    if user["rol"] != "alumno":
        raise HTTPException(status_code=403, detail="Solo los alumnos pueden inscribirse")

    curso = db.query(Course).filter(Course.codigo_acceso == codigo).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    ya_inscrito = db.query(Inscripcion).filter_by(user_id=user["id"], curso_id=curso.id).first()
    if ya_inscrito:
        raise HTTPException(status_code=400, detail="Ya estás inscrito en este curso")

    nueva_inscripcion = Inscripcion(user_id=user["id"], curso_id=curso.id)
    db.add(nueva_inscripcion)
    db.commit()

    return {"mensaje": f"Inscrito correctamente al curso {curso.nombre}"}


def obtener_cursos_inscritos(db: Session, user_id: int):
    return db.query(Inscripcion).filter(Inscripcion.user_id == user_id).all()