from pydantic import BaseModel, EmailStr, Field
from typing import List
from typing import Optional, List
from ..models.user import User

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    roles: List[str] = []
    user_obj: Optional[User] = None   

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    nombre: str = Field(..., min_length=1, max_length=50)
    apellido: str = Field(..., min_length=1, max_length=50)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    nombre: str
    apellido: str
    roles: List[str] = []

    class Config:
        from_attributes = True