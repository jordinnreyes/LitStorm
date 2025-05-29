from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from ..models.user import User
from ..schemas.auth import TokenData
from ..services.user_service import get_user_by_email
from ..db.database import get_db
from sqlalchemy.orm import Session
from .security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_authenticated_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        user = get_user_by_email(db, email)
        if user is None:
            raise credentials_exception

        return user

    except JWTError:
        raise credentials_exception
