from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from bson import ObjectId


class QuizBase(BaseModel):
    titulo: str
    tema: str
    preguntas: List[str]  
    creado_por: str  
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: str = "programado"  


class QuizCreate(QuizBase):
    pass


class QuizInDB(QuizBase):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    creado_en: datetime = Field(default_factory=datetime.now)


class QuizResponse(QuizInDB):
    pass
