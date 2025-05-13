from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db.base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(6), unique=True, index=True, nullable=False)
    docente_id = Column(Integer, nullable=False)  # ID del docente que creó el curso
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    alumnos = relationship("Student", back_populates="curso", cascade="all, delete")