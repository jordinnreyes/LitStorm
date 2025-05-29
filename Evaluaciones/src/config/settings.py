from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    USUARIOS_SERVICE_URL = os.getenv("USUARIOS_SERVICE_URL")
    CURSOS_SERVICE_URL = os.getenv("CURSOS_SERVICE_URL")


settings = Settings()