from pydantic import BaseModel
from typing import List

class UserBase(BaseModel):
    email: str
    nombre: str
    apellido: str

class UserResponse(UserBase):
    id: int
    roles: List[str] = []

    class Config:
        from_attributes = True