from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from bson import ObjectId


class QuizBase(BaseModel):
    titulo: str
    tema: str
    preguntas: List[str]
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: str = "programado"
    curso_id: int

class QuizCreate(QuizBase):
    pass  # Solo para clarificar que es para creación

class QuizInDB(QuizBase):
    creado_por: str
    id: str = Field(default_factory=lambda: str(ObjectId()))
    creado_en: datetime = Field(default_factory=datetime.now)


class QuizResponse(QuizInDB):
    pass

class QuizResumen(BaseModel):
    id: str
    titulo: str
    tema: str
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: str