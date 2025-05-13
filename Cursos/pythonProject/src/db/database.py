from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import settings
from src.db.base import Base

DATABASE_URL = settings.DATABASE_URL

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada")

# Crear motor de conexión
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={"connect_timeout": 5}
)

# Sesión de base de datos
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

# Función para usar en dependencias
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear todas las tablas a partir de los modelos
def create_tables():
    from src.models.course import Course
    from src.models.student import Student
    Base.metadata.create_all(bind=engine)