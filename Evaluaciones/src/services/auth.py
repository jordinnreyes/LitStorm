import requests
from fastapi import HTTPException, Header
from src.config.settings import settings

USUARIOS_SERVICE_URL = settings.USUARIOS_SERVICE_URL
CURSOS_SERVICE_URL = settings.CURSOS_SERVICE_URL  

def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    try:
        res = requests.get(f"{USUARIOS_SERVICE_URL}/auth/validate-token", headers={"Authorization": f"Bearer {token}"})
        if res.status_code != 200:
            raise HTTPException(status_code=401, detail="Token inválido")
        return res.json()
    except:
        raise HTTPException(status_code=500, detail="Error al conectar con servicio de usuarios")

def verificar_curso_existe(curso_id: int):
    url = f"{CURSOS_SERVICE_URL}/cursos/{curso_id}/existe"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        existe = response.json()

        if not existe:
            raise HTTPException(status_code=404, detail="El curso no existe")
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ Error HTTP al verificar curso: {http_err}")
        raise HTTPException(status_code=400, detail="Error al verificar el curso")
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Error de conexión al verificar curso: {req_err}")
        raise HTTPException(status_code=500, detail="No se pudo contactar al servicio de cursos")
