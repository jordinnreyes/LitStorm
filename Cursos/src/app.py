from fastapi import FastAPI
from src.config.settings import settings
from src.db.database import init_db
from src.controllers import cursos, inscripciones

app = FastAPI(
    title="Microservicio de Cursos",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(cursos.router, prefix="/cursos", tags=["cursos"])
app.include_router(inscripciones.router, prefix="/inscripciones", tags=["inscripciones"])
