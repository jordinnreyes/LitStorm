from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from bson import ObjectId

# Usado solo por IA (no requiere curso_id)
class QuestionGenerated(BaseModel):
    texto: str
    opciones: List[str]
    respuesta_correcta: int
    explicacion: str
    tema: str

# Base para almacenamiento y uso interno
class QuestionBase(BaseModel):
    texto: str
    opciones: List[str]
    respuesta_correcta: int
    explicacion: str
    tema: str
    curso_id: int

class QuestionCreate(QuestionBase):
    pass

class QuestionInDB(QuestionBase):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    creado_en: datetime = Field(default_factory=datetime.now)

class QuestionResponse(QuestionInDB):
    pass
