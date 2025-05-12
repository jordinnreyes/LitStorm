from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .db.database import engine, create_tables
from .controllers import auth, users
from fastapi.responses import JSONResponse
import os

# Configuración inicial de la app
app = FastAPI(
    title="Microservicio de Usuarios",
    description="API para gestión de usuarios con autenticación JWT y roles",
    version="1.0.0"
)

# Middleware CORS (ajusta según necesidades)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas en la base de datos (solo para desarrollo)
@app.on_event("startup")
def startup_event():
    if os.getenv("ENVIRONMENT") == "dev":
        create_tables(engine)

# Incluir routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])

# Endpoint de verificación de salud
@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok", "message": "Servicio en ejecución"}

# Manejo de errores global
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )