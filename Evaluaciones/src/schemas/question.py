from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from bson import ObjectId

class QuestionBase(BaseModel):
    texto: str
    opciones: List[str]
    respuesta_correcta: int  
    explicacion: str
    tema: str

class QuestionCreate(QuestionBase):
    pass

class QuestionInDB(QuestionBase):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    creado_en: datetime = Field(default_factory=datetime.now)

class QuestionResponse(QuestionInDB):
    pass
