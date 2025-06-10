from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from bson import ObjectId

class RespuestaAlumno(BaseModel):
    quiz_id: str
    alumno_id: str
    respuestas: List[int]  # Índices de las respuestas en orden

class RespuestaPregunta(BaseModel):
    pregunta_id: str
    respuesta: int  # Índice de la opción seleccionada

class RespuestaQuizCompleto(BaseModel):
    quiz_id: str
    alumno_id: str
    respuestas: List[RespuestaPregunta]  # Lista de respuestas

class RespuestaEnProgreso(BaseModel):
    quiz_id: str
    alumno_id: str
    pregunta_actual: int
    respuesta: int

class ProgresoPregunta(BaseModel):
    respondida: bool
    respuesta: Optional[int] = None

class ProgresoQuiz(BaseModel):
    quiz_id: str
    alumno_id: str
    total_preguntas: int
    pregunta_actual: int
    preguntas_respondidas: int
    progreso: Dict[str, ProgresoPregunta]  # pregunta_id -> estado
    completado: bool = False

class ResultadoPregunta(BaseModel):
    pregunta_id: str
    texto: str
    respuesta_usuario: int  # Índice de la opción seleccionada
    correcta: bool
    explicacion: str
    opciones: List[str] = []  # Texto de las opciones
    respuesta_correcta: int  # Índice de la respuesta correcta
    feedback_ia: Optional[str] = None
    
    class Config:
        json_encoders = {
            ObjectId: str
        }

class ResultadoQuiz(BaseModel):
    quiz_id: str
    alumno_id: str
    puntuacion: int
    total: int
    detalle: List[ResultadoPregunta]
    fecha: datetime
