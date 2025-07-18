FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de la aplicación
WORKDIR /app

# Copiar archivos de dependencias
COPY pyproject.toml .
COPY README.md .

# Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Copiar código fuente
COPY src/ src/

# Crear directorios necesarios
RUN mkdir -p /app/pdfs /app/output

# Variables de entorno por defecto
ENV OCR_ENGINE=donut \
    PDF_DPI=200 \
    USE_GPU=false

# Comando por defecto
CMD ["python", "-m", "src.interfaces.cli"]
