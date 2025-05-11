from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from ..schemas.auth import TokenData
from ..services.user_service import get_user_by_email
from ..db.database import get_db
from sqlalchemy.orm import Session
from security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        roles: list[str] = payload.get("roles", [])
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
        
    return TokenData(
        email=user.email,
        nombre=user.nombre,
        apellido=user.apellido,
        roles=roles,
        user_obj=user
    )

def requires_role(required_role: str):
    def role_checker(current_user: TokenData = Depends(get_current_user)):
        if required_role not in current_user.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires role: {required_role}",
            )
        return current_user.user_obj
    return role_checker