from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CourseCreate(BaseModel):
    nombre: str = Field(..., example="Comunicación | 1° Secundaria Sección A")


class CourseOut(BaseModel):
    id: int
    nombre: str
    codigo: str
    fecha_creacion: datetime

    class Config:
        from_attributes = True


class JoinCourseRequest(BaseModel):
    codigo: str = Field(..., example="ABC123")


class JoinCourseResponse(BaseModel):
    curso_id: int
    nombre: str
    mensaje: str

    class Config:
        from_attributes = True