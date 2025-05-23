from pydantic import BaseModel
from .course import CursoOut

class InscripcionIn(BaseModel):
    curso_id: int

class InscripcionOut(BaseModel):
    id: int
    user_id: int
    curso_id: int
    curso: CursoOut 

    class Config:
        orm_mode = True