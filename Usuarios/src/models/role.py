from sqlalchemy import Column, Integer, String
from .base import Base  

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)  # "admin", "profesor", "alumno"