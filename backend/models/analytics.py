"""
Histórico de notas para projeção IDEB e analytics.
"""
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.sql import func

from backend.database import Base


class GradeHistory(Base):
    __tablename__ = "grade_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer)
    activity_name = Column(String(255))
    grade = Column(Float)
    max_grade = Column(Float)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
