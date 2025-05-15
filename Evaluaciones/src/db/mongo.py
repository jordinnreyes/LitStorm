from motor.motor_asyncio import AsyncIOMotorClient
from ..config.settings import settings

MONGO_URI = settings.MONGO_URI
MONGO_DB_NAME = settings.MONGO_DB_NAME

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]

# Acceso directo a colecciones
preguntas_collection = db["preguntas"]
quizzes_collection = db["quizzes"]
