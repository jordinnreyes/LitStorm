from http.client import HTTPException
from typing import List
from openai import AsyncOpenAI
import json
from src.schemas.question import QuestionCreate, QuestionGenerated
from ..config.settings import settings
from openai import OpenAIError
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

#funcion para generar las pregutnas con la Ia
async def generar_preguntas_con_ia(tema: str, cantidad: int = 5) -> List[QuestionGenerated]:
    prompt = (
        f"Genera {cantidad} preguntas de opción múltiple sobre el tema: '{tema}'.\n"
        "Devuelve cada pregunta con los siguientes campos en formato JSON:\n"
        "- texto: enunciado de la pregunta\n"
        "- opciones: lista de 4 opciones\n"
        "- respuesta_correcta: índice correcto (0-3)\n"
        "- explicacion: por qué es correcta la respuesta\n"
        "Devuélvelo como una lista JSON válida. No agregues texto adicional."
    )

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message.content.strip()
        print("📥 Respuesta cruda de la IA:\n", content)

        try:
            preguntas_raw = json.loads(content)
        except json.JSONDecodeError as je:
            raise HTTPException(status_code=500, detail=f"JSON inválido: {je.msg}")

        preguntas = []
        for i, item in enumerate(preguntas_raw):
            pregunta = QuestionGenerated(
                texto=item["texto"],
                opciones=item["opciones"],
                respuesta_correcta=item["respuesta_correcta"],
                explicacion=item["explicacion"],
                tema=tema
            )
            preguntas.append(pregunta)
        return preguntas

    except OpenAIError as oe:
        # Aquí puedes detectar si es un error de saldo o cuota
        error_msg = str(oe)
        print(f"❌ Error de OpenAI: {error_msg}")

        if "quota" in error_msg.lower() or "insufficient" in error_msg.lower():
            raise HTTPException(status_code=402, detail="Crédito insuficiente en la API de OpenAI.")
        else:
            raise HTTPException(status_code=500, detail=f"Error de OpenAI: {error_msg}")
    except Exception as e:
        print(f"❌ Error inesperado al generar preguntas: {e}")
        raise HTTPException(status_code=500, detail="Error inesperado al generar preguntas.")
    

#Da el feedback para las preguntas que hubo error
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
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error al generar feedback IA: {e}")
        return "No se pudo generar feedback en este momento."
