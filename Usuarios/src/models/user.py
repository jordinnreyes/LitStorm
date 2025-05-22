# models/user.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .role import Role


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    hashed_password = Column(String(200), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id")) 
    
    role = relationship(Role, back_populates="users")