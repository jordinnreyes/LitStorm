import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config.settings import settings

DATABASE_URL = settings.DATABASE_URL

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada en .env")


engine = create_engine(
    DATABASE_URL,
    pool_size=40,            
    max_overflow=10,         
    pool_pre_ping=True,      
    pool_recycle=3600,       
    connect_args={
        "connect_timeout": 5 
    }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False 
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()