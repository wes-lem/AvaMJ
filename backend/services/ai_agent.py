"""
Lógica do Professor Virtual (OpenAI).
"""
from backend.config import settings


async def get_ai_response(user_id: int, message: str) -> str:
    """
    Envia a mensagem do aluno para a OpenAI e retorna a resposta
    do Professor Virtual (contexto educacional).
    """
    if not settings.OPENAI_API_KEY:
        return "O Professor Virtual está indisponível no momento. Configure OPENAI_API_KEY."

    # openai.ChatCompletion.create(...) com system prompt de tutor
    # Exemplo: role="assistant", content="Você é um professor virtual..."
    return "Resposta da IA (implementar chamada OpenAI)."
