FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema para psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Configurar PYTHONPATH para que encuentre los módulos en src/
ENV PYTHONPATH=/app/src

# Comando corregido para apuntar a src/app.py
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]