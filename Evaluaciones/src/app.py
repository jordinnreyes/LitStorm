from fastapi import FastAPI
from src.controllers import question_controller, quiz_controller
from src.controllers import respuesta_controller

app = FastAPI(
    title="Microservicio de Evaluciones",
    version="1.0.0"
)

app.include_router(question_controller.router)
app.include_router(quiz_controller.router)
app.include_router(respuesta_controller.router)