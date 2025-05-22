from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    USUARIOS_SERVICE_URL = os.getenv("USUARIOS_SERVICE_URL")



settings = Settings()