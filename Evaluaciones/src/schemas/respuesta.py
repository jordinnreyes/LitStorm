from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class RespuestaAlumno(BaseModel):
    quiz_id: str
    alumno_id: str
    respuestas: List[int]

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
    texto: str
    correcta: bool
    respuesta_usuario: str
    respuesta_correcta: str
    explicacion: str
    feedback_ia: Optional[str] = None

class ResultadoQuiz(BaseModel):
    quiz_id: str
    alumno_id: str
    puntuacion: int
    total: int
    detalle: List[ResultadoPregunta]
    fecha: datetime
