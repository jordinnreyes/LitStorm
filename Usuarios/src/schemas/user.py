from pydantic import BaseModel, EmailStr, Field, model_serializer
from typing import Optional
from .role import RoleName

class UserBase(BaseModel):
    email: EmailStr
    nombre: str = Field(..., min_length=1, max_length=50)
    apellido: str = Field(..., min_length=1, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role: RoleName

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombre: Optional[str] = Field(None, min_length=1, max_length=50)
    apellido: Optional[str] = Field(None, min_length=1, max_length=50)
    role: Optional[RoleName] = None

class UserResponse(UserBase):
    id: int
    role: str

    @model_serializer(mode="plain")
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "role": (
                self.role.value if isinstance(self.role, RoleName)
                else str(self.role)
            )
        }