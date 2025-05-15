from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RespuestaAlumno(BaseModel):
    quiz_id: str
    alumno_id: str
    respuestas: List[int]  

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
