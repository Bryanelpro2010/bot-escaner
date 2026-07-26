# Usamos una imagen base de Python con soporte para herramientas de sistema
FROM python:3.10-slim

# Instalar la pantalla invisible (Xvfb) y dependencias del sistema sin borrar nada
RUN apt-get update && apt-get install -y \
    xvfb \
    x11-utils \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Definir el directorio de trabajo
WORKDIR /app

# Copiar tus archivos actuales al contenedor
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Variables de entorno para la pantalla invisible
ENV DISPLAY=:99
ENV PYTHONUNBUFFERED=1

# Comando para iniciar la pantalla invisible en memoria RAM y correr tu main.py
CMD Xvfb :99 -screen 0 1024x768x16 & python -u main.py
