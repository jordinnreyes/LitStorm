import random
import string
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models.course import Course
from src.models.student import Student
from src.schemas.course import CourseCreate


# Función para generar un código alfanumérico único
def generar_codigo_curso(longitud: int = 6) -> str:
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choices(caracteres, k=longitud))


# Crear un curso (solo docentes)
def crear_curso(db: Session, curso_data: CourseCreate, docente_id: int) -> Course:
    # Generar código único (verificar colisión)
    while True:
        codigo = generar_codigo_curso()
        if not db.query(Course).filter_by(codigo=codigo).first():
            break

    nuevo_curso = Course(
        nombre=curso_data.nombre,
        codigo=codigo,
        docente_id=docente_id
    )
    db.add(nuevo_curso)
    db.commit()
    db.refresh(nuevo_curso)
    return nuevo_curso


# Unir a un alumno a un curso usando el código
def unir_alumno_a_curso(db: Session, codigo: str, alumno_data: dict) -> Student:
    curso = db.query(Course).filter_by(codigo=codigo).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Código de curso inválido")

    # Verificar si ya está inscrito (por email o ID)
    ya_inscrito = db.query(Student).filter_by(email=alumno_data["email"]).first()
    if ya_inscrito:
        raise HTTPException(status_code=400, detail="Ya estás inscrito en un curso")

    alumno = Student(
        email=alumno_data["email"],
        nombre=alumno_data["nombre"],
        apellido=alumno_data["apellido"],
        course_id=curso.id
    )
    db.add(alumno)
    db.commit()
    db.refresh(alumno)
    return alumno, curso