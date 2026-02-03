"""
Tabelas de XP, Medalhas e Níveis (gamificação).
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.database import Base


class XP(Base):
    __tablename__ = "xp"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    points = Column(Integer, default=0)
    source = Column(String(100))  # ex: "nota_80", "frequencia"
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100))   # ex: "Ouro", "Prata", "Bronze"
    type = Column(String(50))    # ex: "nota", "frequencia"
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    level = Column(Integer, default=1)
    total_xp = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
