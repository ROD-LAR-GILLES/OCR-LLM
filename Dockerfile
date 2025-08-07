FROM python:3.11-slim
FROM python:3.11-slim
# Install system dependencies
RUN apt-get update && apt-get install -y \rias
    curl \ apt-get install -y \
    gcc \ \
    g++ \er-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better cachingctorio de la aplicación
COPY requirements.txt .WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
os
# Copy application codeCOPY pyproject.toml ocr_donut.py ./
COPY src/ ./src/
COPY tests/ ./tests/

# Create necessary directoriesorg/whl/cpu && \
RUN mkdir -p /app/pdfs /app/output /app/logs    pip install --no-cache-dir transformers pdf2image pillow python-dotenv protobuf sentencepiece

# Add non-root usersultados
RUN useradd -m -u 1000 ocruser && chown -R ocruser:ocruser /appRUN mkdir -p /app/pdfs /app/output
USER ocruser
torno
# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \    MODEL_NAME="naver-clova-ix/donut-base"
    CMD curl -f http://localhost:8000/health || exit 1

# Expose portVOLUME ["/app/pdfs", "/app/output"]
EXPOSE 8000
ndo
# Start applicationCMD ["tail", "-f", "/dev/null"]


CMD ["uvicorn", "src.interfaces.api.main:app", "--host", "0.0.0.0", "--port", "8000"]