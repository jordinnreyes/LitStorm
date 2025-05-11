from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    hashed_password = Column(String(200))
    
    # Relación muchos-a-muchos con roles (tabla intermedia automática)
    roles = relationship("Role", secondary="user_roles")