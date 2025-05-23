from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.base import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    profesor_id = Column(Integer, nullable=False)  # el profesor se une automaticamente
    codigo_acceso = Column(String, unique=True, nullable=False)  # Clave para que los alumnos entren
    

    inscripciones = relationship("Inscripcion", back_populates="curso")

