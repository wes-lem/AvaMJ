"""
Entrega JSON de pontos, ranking e medalhas.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db

router = APIRouter()


@router.get("/ranking")
def get_ranking(db: Session = Depends(get_db)):
    """Lista ranking por XP total."""
    return {"ranking": [], "message": "Implementar query de ranking"}


@router.get("/user/{user_id}/xp")
def get_user_xp(user_id: int, db: Session = Depends(get_db)):
    """Retorna XP e nível do usuário."""
    return {"user_id": user_id, "xp": 0, "level": 1}


@router.get("/user/{user_id}/badges")
def get_user_badges(user_id: int, db: Session = Depends(get_db)):
    """Retorna medalhas do usuário."""
    return {"user_id": user_id, "badges": []}
