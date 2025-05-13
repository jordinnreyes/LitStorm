from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from src.config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # El endpoint de login es de usuarios

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("id")
        email = payload.get("sub")
        nombre = payload.get("nombre")
        apellido = payload.get("apellido")
        rol = payload.get("rol")

        if not all([user_id, email, nombre, apellido, rol]):
            raise credentials_exception

        return {
            "id": user_id,
            "email": email,
            "nombre": nombre,
            "apellido": apellido,
            "rol": rol
        }

    except JWTError:
        raise credentials_exception