from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config.settings import settings
from models.base import Base
from models.user import User 
from models.role import Role
from sqlalchemy.orm import Session

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

def init_roles(db: Session):
    # Verificar si los roles ya existen
    for role_name in ["admin", "alumno", "profesor"]:
        role_exists = db.query(Role).filter(Role.name == role_name).first()
        if not role_exists:
            # Si no existe, agregarlo
            new_role = Role(name=role_name)
            db.add(new_role)
            db.commit()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables(engine):
    Base.metadata.create_all(bind=engine)