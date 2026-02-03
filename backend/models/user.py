"""
Tabela de Alunos (sincronizada com Moodle).
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    moodle_id = Column(Integer, unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    full_name = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
