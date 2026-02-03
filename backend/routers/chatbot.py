"""
Rota da IA (OpenAI) – Professor Virtual.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# from backend.services.ai_agent import get_ai_response

router = APIRouter()


class ChatMessage(BaseModel):
    user_id: int
    message: str


@router.post("/message")
async def send_message(payload: ChatMessage):
    """Envia mensagem ao chatbot e retorna resposta da IA."""
    # response = await get_ai_response(payload.user_id, payload.message)
    return {"reply": "Resposta do Professor Virtual (implementar OpenAI)", "user_id": payload.user_id}
