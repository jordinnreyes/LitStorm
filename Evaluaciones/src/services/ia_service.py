<<<<<<< HEAD
from http.client import HTTPException
from typing import List
from openai import AsyncOpenAI
import json
from src.schemas.question import QuestionCreate, QuestionGenerated
from ..config.settings import settings
from openai import OpenAIError
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def generar_preguntas_con_ia(tema: str, cantidad: int = 5) -> List[QuestionGenerated]:
=======
from typing import List
from openai import AsyncOpenAI
import json
from src.schemas.question import QuestionCreate
from ..config.settings import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def generar_preguntas_con_ia(tema: str, cantidad: int = 5) -> List[QuestionCreate]:
>>>>>>> 96bd197fb810fc04029f0363761fccd31aa3470a
    prompt = (
        f"Genera {cantidad} preguntas de opción múltiple sobre el tema: '{tema}'.\n"
        "Devuelve cada pregunta con los siguientes campos en formato JSON:\n"
        "- texto: enunciado de la pregunta\n"
        "- opciones: lista de 4 opciones\n"
        "- respuesta_correcta: índice correcto (0-3)\n"
        "- explicacion: por qué es correcta la respuesta\n"
<<<<<<< HEAD
        "Devuélvelo como una lista JSON válida. No agregues texto adicional."
=======
        "Devuélvelo como una lista JSON válida."
>>>>>>> 96bd197fb810fc04029f0363761fccd31aa3470a
    )

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
<<<<<<< HEAD
        content = response.choices[0].message.content.strip()
        print("📥 Respuesta cruda de la IA:\n", content)

        try:
            preguntas_raw = json.loads(content)
        except json.JSONDecodeError as je:
            raise HTTPException(status_code=500, detail=f"JSON inválido: {je.msg}")

        preguntas = []
        for i, item in enumerate(preguntas_raw):
            pregunta = QuestionGenerated(
=======

        content = response.choices[0].message.content.strip()
        preguntas_raw = json.loads(content)

        preguntas = []
        for item in preguntas_raw:
            pregunta = QuestionCreate(
>>>>>>> 96bd197fb810fc04029f0363761fccd31aa3470a
                texto=item["texto"],
                opciones=item["opciones"],
                respuesta_correcta=item["respuesta_correcta"],
                explicacion=item["explicacion"],
                tema=tema
            )
            preguntas.append(pregunta)
<<<<<<< HEAD
        return preguntas

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
    

=======

        return preguntas

    except json.JSONDecodeError:
        print("❌ La IA respondió con un JSON inválido.")
        return []
    except Exception as e:
        print(f"❌ Error inesperado al generar preguntas: {e}")
        return []
>>>>>>> 96bd197fb810fc04029f0363761fccd31aa3470a

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
