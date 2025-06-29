from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from openai import AsyncOpenAI, OpenAIError
from ..config.settings import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

class ChatMessage(BaseModel):
    role: str  
    content: str

class ChatResponse(BaseModel):
    role: str  
    content: str

router = APIRouter(prefix="/chatbot", tags=["ChatBot"])

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(mensajes: List[ChatMessage]):
    system_prompt = {
        "role": "system",
        "content": (
            "Eres un asistente educativo especializado en el curso de Comunicación del currículo escolar peruano. "
            "Responde únicamente preguntas relacionadas a ese curso. Si la pregunta no es relevante, responde con amabilidad que no puedes ayudar con eso."
        )
    }

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[system_prompt] + [m.dict() for m in mensajes],
            temperature=0.7
        )
        mensaje_ia = response.choices[0].message
        return ChatResponse(
            role=mensaje_ia.role,
            content=mensaje_ia.content.strip()
        )

    except OpenAIError as oe:
        error_msg = str(oe)
        print(f"❌ Error OpenAI: {error_msg}")
        if "quota" in error_msg.lower() or "insufficient" in error_msg.lower():
            raise HTTPException(status_code=402, detail="Crédito insuficiente en la API de OpenAI.")
        raise HTTPException(status_code=500, detail=f"Error con OpenAI: {error_msg}")

    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        raise HTTPException(status_code=500, detail="Error inesperado al generar respuesta del chatbot.")
