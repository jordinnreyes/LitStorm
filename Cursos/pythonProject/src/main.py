from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db.database import create_tables, engine
from src.routers.course_router import router as course_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(
    title="API Cursos - LitStorm",
    description="Microservicio para gestión de cursos",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar el router
app.include_router(course_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API Cursos funcionando"}