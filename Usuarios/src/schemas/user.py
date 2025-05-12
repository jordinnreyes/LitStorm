from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from .role import RoleName  # Importamos la validación de roles

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
    
    class Config:
        from_attributes = True
        
        @classmethod
        def model_validate(cls, obj):
            if hasattr(obj, 'role'):
                obj.role = obj.role.name if obj.role else None
            return super().model_validate(obj)