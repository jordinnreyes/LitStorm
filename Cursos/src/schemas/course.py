from pydantic import BaseModel

class CursoBase(BaseModel):
    nombre: str
    descripcion: str | None = None

class CursoOut(CursoBase):
    id: int
    profesor_id: int
    codigo_acceso: str

    class Config:
        orm_mode = True