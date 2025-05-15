from fastapi import FastAPI
from src.controllers import question_controller, quiz_controller
from src.controllers import respuesta_controller


app = FastAPI()

app.include_router(question_controller.router)
app.include_router(quiz_controller.router)
app.include_router(respuesta_controller.router)
