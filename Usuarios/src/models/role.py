from sqlalchemy import Column, Integer, String
from .base import Base  
from sqlalchemy.orm import relationship

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True) 

    users = relationship("User", back_populates="role")