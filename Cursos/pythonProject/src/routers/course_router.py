from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.schemas.course import (
    CourseCreate, CourseOut, JoinCourseRequest, JoinCourseResponse
)
from src.services.course_service import crear_curso, unir_alumno_a_curso
from src.utils.token_verifier import get_current_user

router = APIRouter(prefix="/courses", tags=["courses"])


# Endpoint: Crear un curso (solo docentes)
@router.post("/", response_model=CourseOut)
def crear_nuevo_curso(
    curso_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["rol"] != "docente":
        raise HTTPException(status_code=403, detail="Solo los docentes pueden crear cursos")

    nuevo_curso = crear_curso(db, curso_data, docente_id=current_user["id"])
    return nuevo_curso


# Endpoint: Unirse a un curso por código (solo alumnos)
@router.post("/join", response_model=JoinCourseResponse)
def unirse_a_curso(
    data: JoinCourseRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["rol"] != "alumno":
        raise HTTPException(status_code=403, detail="Solo los alumnos pueden unirse a cursos")

    alumno_data = {
        "email": current_user["email"],
        "nombre": current_user["nombre"],
        "apellido": current_user["apellido"]
    }

    alumno, curso = unir_alumno_a_curso(db, data.codigo, alumno_data)

    return JoinCourseResponse(
        curso_id=curso.id,
        nombre=curso.nombre,
        mensaje=f"Te uniste correctamente al curso: {curso.nombre}"
    )


# Endpoint: Obtener cursos propios (para docentes)
@router.get("/mine", response_model=list[CourseOut])
def obtener_cursos_propios(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["rol"] != "docente":
        raise HTTPException(status_code=403, detail="Solo los docentes pueden consultar sus cursos")

    cursos = db.query(CourseOut.__annotations__).filter_by(docente_id=current_user["id"]).all()
    return cursos