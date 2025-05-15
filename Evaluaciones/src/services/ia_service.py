from typing import List
import openai
import json
from src.schemas.question import QuestionCreate
from ..config.settings import settings

openai.api_key = settings.OPENAI_API_KEY  

async def generar_preguntas_con_ia(tema: str, cantidad: int = 5) -> List[QuestionCreate]:
    prompt = (
        f"Genera {cantidad} preguntas de opción múltiple sobre el tema: '{tema}'.\n"
        "Devuelve cada pregunta con los siguientes campos en formato JSON:\n"
        "- texto: enunciado de la pregunta\n"
        "- opciones: lista de 4 opciones\n"
        "- respuesta_correcta: índice correcto (0-3)\n"
        "- explicacion: por qué es correcta la respuesta\n"
        "Devuélvelo como una lista JSON válida."
    )

    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        content = response.choices[0].message.content.strip()

        # Intentamos parsear como JSON
        preguntas_raw = json.loads(content)

        # Validamos cada pregunta con el esquema de Pydantic
        preguntas = []
        for item in preguntas_raw:
            pregunta = QuestionCreate(
                texto=item["texto"],
                opciones=item["opciones"],
                respuesta_correcta=item["respuesta_correcta"],
                explicacion=item["explicacion"],
                tema=tema
            )
            preguntas.append(pregunta)

        return preguntas

    except json.JSONDecodeError:
        print("❌ La IA respondió con un JSON inválido.")
        return []
    except Exception as e:
        print(f"❌ Error inesperado al generar preguntas: {e}")
        return []


async def generar_feedback_ia(pregunta: str, opciones: list, correcta: int, seleccionada: int) -> str:
    prompt = (
        f"La siguiente pregunta fue respondida incorrectamente por un estudiante:\n"
        f"Pregunta: {pregunta}\n"
        f"Opciones: {opciones}\n"
        f"Opción seleccionada: {opciones[seleccionada]}\n"
        f"Opción correcta: {opciones[correcta]}\n"
        f"Explica de forma breve por qué el estudiante falló y cuál era la lógica correcta."
    )

    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error al generar feedback IA: {e}")
        return "No se pudo generar feedback en este momento."
