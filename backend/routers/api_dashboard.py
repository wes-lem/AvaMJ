"""
Entrega JSON de notas e frequência para o dashboard.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db

router = APIRouter()


@router.get("/user/{user_id}/grades")
def get_user_grades(user_id: int, db: Session = Depends(get_db)):
    """Notas do aluno para gráficos."""
    return {"user_id": user_id, "grades": [], "frequency": []}


@router.get("/user/{user_id}/summary")
def get_dashboard_summary(user_id: int, db: Session = Depends(get_db)):
    """Resumo: média, evolução, projeção IDEB."""
    return {"user_id": user_id, "average": 0, "trend": "stable"}
