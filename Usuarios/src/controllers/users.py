from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models.user import User
from ..db.database import get_db
from ..schemas.user import UserResponse
from ..utils.dependencies import get_authenticated_user
from ..models.role import Role

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def read_current_user(
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    # Obtener el nombre del rol desde la base de datos
    role = db.query(Role).filter(Role.id == current_user.role_id).first()
    role_name = role.name if role else "usuario"

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        nombre=current_user.nombre,
        apellido=current_user.apellido,
        role=role_name
    )

