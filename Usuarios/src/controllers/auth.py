from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..schemas.auth import Token
from ..schemas.user import UserCreate
from ..services.auth_service import register_user, authenticate_user
from ..utils.security import create_access_token

router = APIRouter(tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,  
    db: Session = Depends(get_db)
):
    try:
        user = register_user(db, user_data)
        return {
            "message": "Usuario registrado",
            "user_id": user.id,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "role": user.role_id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    
    access_token = create_access_token(
        data={
            "sub": user.email,
            "nombre": user.nombre,
            "role": user.role_id
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}