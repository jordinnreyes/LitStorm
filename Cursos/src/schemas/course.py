from pydantic import BaseModel
from typing import Optional

class CursoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CursoOut(CursoBase):
    id: int
    class Config:
        orm_mode = True
