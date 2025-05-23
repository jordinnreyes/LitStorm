from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.db.base import Base


class Inscripcion(Base):
    __tablename__ = "inscripciones"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    curso_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    curso = relationship("Course", back_populates="inscripciones")