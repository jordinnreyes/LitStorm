import requests
from fastapi import HTTPException, Header
from src.config.settings import settings

USUARIOS_SERVICE_URL = settings.USUARIOS_SERVICE_URL

def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    try:
        res = requests.get(f"{USUARIOS_SERVICE_URL}/auth/validate-token", headers={"Authorization": f"Bearer {token}"})
        if res.status_code != 200:
            raise HTTPException(status_code=401, detail="Token inválido")
        return res.json()
    except:
        raise HTTPException(status_code=500, detail="Error al conectar con servicio de usuarios")
