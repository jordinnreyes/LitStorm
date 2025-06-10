from bson import ObjectId
from ..models.quiz import get_quiz_document
from ..db.mongo import quizzes_collection, preguntas_collection, respuestas_collection
from ..schemas.quiz import QuizCreate
from ..schemas.respuesta import ProgresoQuiz, ProgresoPregunta
from typing import Optional, List, Dict, Tuple
from datetime import datetime
from ..utils.estado_quiz import determinar_estado

#Endpoint para poder crear un quiz (funciona)
async def crear_quiz(quiz_data: QuizCreate, creado_por: str) -> Optional[str]:
    try:
        preguntas_ids = [ObjectId(pid) for pid in quiz_data.preguntas]

        quiz_doc = get_quiz_document(
            titulo=quiz_data.titulo,
            tema=quiz_data.tema,
            preguntas=preguntas_ids,
            creado_por=creado_por,
            curso_id=quiz_data.curso_id,
            fecha_inicio=quiz_data.fecha_inicio,
            fecha_fin=quiz_data.fecha_fin,
            estado=quiz_data.estado
        )

        result = await quizzes_collection.insert_one(quiz_doc)
        return str(result.inserted_id)
    
    except Exception as e:
        print(f"Error creando quiz: {e}")
        return None

#Endpoint para tener 1 a 1 las preguntas del quiz
async def obtener_quiz_para_alumno(quiz_id: str, alumno_id: str) -> Dict:
    try:
        # Obtener el quiz
        quiz = await quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
        if not quiz:
            raise ValueError("Quiz no encontrado")

        # Obtener o crear el progreso del alumno
        progreso = await obtener_o_crear_progreso(quiz_id, alumno_id, len(quiz["preguntas"]))
        
        if progreso.completado:
            raise ValueError("Ya has completado este quiz")

        # Obtener la pregunta actual
        pregunta_actual = await preguntas_collection.find_one(
            {"_id": quiz["preguntas"][progreso.pregunta_actual]},
            {"texto": 1, "opciones": 1, "_id": 1}
        )

        return {
            "id": str(quiz["_id"]),
            "titulo": quiz["titulo"],
            "tema": quiz["tema"],
            "pregunta_actual": {
                "numero": progreso.pregunta_actual + 1,
                "total": progreso.total_preguntas,
                "id": str(pregunta_actual["_id"]),
                "texto": pregunta_actual["texto"],
                "opciones": pregunta_actual["opciones"]
            },
            "progreso": {
                "preguntas_respondidas": progreso.preguntas_respondidas,
                "total_preguntas": progreso.total_preguntas,
                "porcentaje": (progreso.preguntas_respondidas / progreso.total_preguntas) * 100
            }
        }

    except ValueError as e:
        raise e
    except Exception as e:
        print(f"Error obteniendo quiz: {e}")
        raise Exception("Error interno obteniendo el quiz")

#Funcion para guardar el progreso
async def obtener_o_crear_progreso(quiz_id: str, alumno_id: str, total_preguntas: int) -> ProgresoQuiz:
    """
    Obtiene o crea el progreso de un alumno en un quiz.
    """
    # Aquí deberías tener una colección para guardar el progreso
    # Por ahora usaremos una variable en memoria (en producción esto debería estar en la base de datos)
    progreso = ProgresoQuiz(
        quiz_id=quiz_id,
        alumno_id=alumno_id,
        total_preguntas=total_preguntas,
        pregunta_actual=0,
        preguntas_respondidas=0,
        progreso={}
    )
    return progreso

#Guarda la respuesta de cada pregunta del alumno
async def guardar_respuesta_pregunta(quiz_id: str, alumno_id: str, pregunta_id: str, respuesta: int) -> ProgresoQuiz:
    """
    Guarda la respuesta a una pregunta y actualiza el progreso.
    """
    # Aquí deberías actualizar el progreso en la base de datos
    # Por ahora solo retornamos un progreso simulado
    return ProgresoQuiz(
        quiz_id=quiz_id,
        alumno_id=alumno_id,
        total_preguntas=5,  # Este valor debería venir de la base de datos
        pregunta_actual=1,  # Incrementado
        preguntas_respondidas=1,
        progreso={
            pregunta_id: ProgresoPregunta(respondida=True, respuesta=respuesta)
        }
    )


#Funcion para saber los quizes que estan activos / programados (funciona)
async def obtener_quizzes_activos_programados(curso_id: int) -> List[dict]:
    ahora = datetime.now()
    cursor = quizzes_collection.find({
        "curso_id": curso_id,
        "fecha_fin": {"$gte": ahora}
    })

    quizzes = []
    async for quiz in cursor:
        estado_actual = determinar_estado(quiz["fecha_inicio"], quiz["fecha_fin"])
        if estado_actual in ("activo", "programado"):  # traer ambos
            quizzes.append({
                "id": str(quiz["_id"]),
                "titulo": quiz["titulo"],
                "tema": quiz["tema"],
                "fecha_inicio": quiz["fecha_inicio"],
                "fecha_fin": quiz["fecha_fin"],
                "estado": estado_actual
            })

    return quizzes

async def obtener_preguntas_quiz(quiz_id: str) -> List[Dict]:
    """
    Obtiene todas las preguntas de un quiz incluyendo las respuestas correctas.
    """
    try:
        # Obtener el quiz
        quiz = await quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
        if not quiz:
            raise ValueError("Quiz no encontrado")

        # Obtener todas las preguntas del quiz
        preguntas_ids = [ObjectId(pid) for pid in quiz["preguntas"]]
        preguntas = []
        
        # Obtener cada pregunta incluyendo la respuesta correcta
        for pregunta_id in preguntas_ids:
            pregunta = await preguntas_collection.find_one({"_id": pregunta_id})
            if pregunta:
                preguntas.append({
                    "id": str(pregunta["_id"]),
                    "texto": pregunta["texto"],
                    "opciones": pregunta["opciones"],
                    "tema": pregunta.get("tema", ""),
                    "explicacion": pregunta.get("explicacion", ""),
                    "respuesta_correcta": pregunta.get("respuesta_correcta", None)
                })
        
        if not preguntas:
            raise ValueError("No se encontraron preguntas para este quiz")
            
        return preguntas
        
    except ValueError as e:
        raise e
    except Exception as e:
        print(f"Error obteniendo preguntas del quiz: {e}")
        raise Exception("Error interno obteniendo las preguntas del quiz")

async def obtener_respuestas_quiz(quiz_id: str) -> Dict:
    """
    Obtiene todas las respuestas de un quiz.
    Muestra todas las respuestas sin filtrar por rol.
    """
    try:
        # Verificar que el quiz existe
        quiz = await quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
        if not quiz:
            raise ValueError("Quiz no encontrado")

        # Obtener todas las respuestas
        respuestas = await respuestas_collection.find({"quiz_id": quiz_id}).to_list(None)
        
        # Obtener detalles de las preguntas para cada respuesta
        respuestas_detalladas = []
        
        for respuesta in respuestas:
            # Obtener detalles de las preguntas
            preguntas = []
            for detalle in respuesta.get("detalle", []):
                pregunta = await preguntas_collection.find_one({"_id": ObjectId(detalle["pregunta_id"])})
                if pregunta:
                    preguntas.append({
                        "pregunta_id": str(pregunta["_id"]),
                        "texto": pregunta["texto"],
                        "opciones": pregunta["opciones"],
                        "respuesta_usuario": detalle.get("respuesta_usuario", ""),
                        "correcta": detalle.get("correcta", False),
                        "explicacion": detalle.get("explicacion", "")
                    })
            
            respuestas_detalladas.append({
                "alumno_id": respuesta["alumno_id"],
                "preguntas": preguntas,
                "puntuacion": respuesta.get("puntuacion", 0),
                "total": respuesta.get("total", 0),
                "fecha": respuesta.get("fecha", datetime.now())
            })
        
        return {
            "quiz_id": str(quiz["_id"]),
            "titulo": quiz["titulo"],
            "respuestas": respuestas_detalladas
        }
            
    except ValueError as e:
        raise e
    except Exception as e:
        print(f"Error obteniendo respuestas del quiz: {e}")
        raise Exception("Error interno obteniendo las respuestas del quiz")


async def obtener_temas_quizzes() -> List[str]:
    """
    Obtiene una lista de todos los temas únicos de los quizzes existentes.
    
    Returns:
        List[str]: Lista de temas únicos ordenados alfabéticamente
    """
    try:
        # Usamos distinct para obtener valores únicos del campo 'tema'
        temas = await quizzes_collection.distinct("tema")
        
        # Filtramos valores nulos o vacíos y ordenamos alfabéticamente
        temas_filtrados = sorted([t for t in temas if t and t.strip()])
        
        return temas_filtrados
        
    except Exception as e:
        print(f"Error obteniendo temas de quizzes: {e}")
        raise Exception("Error interno obteniendo los temas de los quizzes")

