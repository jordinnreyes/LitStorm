from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.base import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    

    inscripciones = relationship("Inscripcion", back_populates="curso")

