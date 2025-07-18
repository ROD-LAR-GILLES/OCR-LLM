FROM python:3.11-slim

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    poppler-utils \
    gcc \
    python3-dev \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de la aplicación
WORKDIR /app

# Copiar solo los archivos necesarios
COPY pyproject.toml ocr_donut.py ./

# Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir transformers pdf2image pillow python-dotenv protobuf sentencepiece

# Crear directorios para PDFs y resultados
RUN mkdir -p /app/pdfs /app/output

# Variables de entorno
ENV PDF_DPI=200 \
    MODEL_NAME="naver-clova-ix/donut-base"

# Volúmenes para PDFs y resultados
VOLUME ["/app/pdfs", "/app/output"]

# Mantener el contenedor corriendo
CMD ["tail", "-f", "/dev/null"]
