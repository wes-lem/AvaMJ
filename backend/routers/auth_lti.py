"""
Recebe o aluno vindo do Moodle (LTI Launch).
"""
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from backend.database import get_db

router = APIRouter()


@router.post("/lti/launch")
async def lti_launch(request: Request, db: Session = Depends(get_db)):
    """Processa o launch LTI e cria/atualiza o usuário a partir do Moodle."""
    # body = await request.form()
    # lis_person_sourcedid, email, name_full = ...
    # criar ou atualizar User no banco
    return {"status": "ok", "message": "LTI launch (implementar parsing)"}
