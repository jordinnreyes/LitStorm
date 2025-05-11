from fastapi import FastAPI
from .models.user import Base
from config.database import engine

app = FastAPI(title="Microservicio de Usuarios")

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Bienvenido al microservicio de usuarios"}