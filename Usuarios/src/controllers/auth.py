from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..schemas.auth import Token
from ..schemas.user import UserCreate, UserResponse, LoginRequest
from ..services.auth_service import register_user, authenticate_user
from ..utils.security import create_access_token
from ..config.settings import settings
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from ..models.role import Role



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


SECRET_KEY = settings.SECRET_KEY

router = APIRouter(tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = register_user(db, user_data)  # Se registra el usuario

        # Ahora que la relación 'role' está cargada, accedemos al nombre del rol
        return UserResponse(
            id=user.id,
            email=user.email,
            nombre=user.nombre,
            apellido=user.apellido,
            role=user.role.name  # Aquí accedemos al 'name' del rol, no al 'id'
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,  
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    
    role = db.query(Role).filter(Role.id == user.role_id).first()
    role_name = role.name if role else "usuario"
    
    access_token = create_access_token(
        data={
            "id": user.id,
            "sub": user.email,
            "nombre": user.nombre,
            "role": role_name,
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}


# En usuarios/controllers/auth.py

@router.get("/validate-token")
def validate_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {
            "id": payload.get("id"),
            "email": payload.get("sub"),
            "rol": payload.get("role"),
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
