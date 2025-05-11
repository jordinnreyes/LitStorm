from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..schemas.user import UserResponse
from ..services.user_service import get_user_profile
from ..utils.dependencies import requires_role

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def read_current_user(
    current_user: UserResponse = Depends(requires_role("alumno"))  
):
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(requires_role("admin"))  
):
    user = get_user_profile(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user