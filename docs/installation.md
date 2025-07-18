# Guía de Instalación

## Requisitos del Sistema

- Python 3.10 o superior
- Redis (opcional, para caché)
- Docker (opcional, para contenedores)

## Instalación desde PyPI

```bash
pip install ocr-llm-cli
```

## Instalación desde el Código Fuente

1. Clonar el repositorio:
```bash
git clone https://github.com/ROD-LAR-GILLES/OCR-LLM.git
cd OCR-LLM
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -e ".[dev]"
```

## Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Configuración de Donut
MODEL_NAME=naver-clova-ix/donut-base-finetuned-cord-v2
USE_GPU=true
PDF_DPI=200
MAX_OUTPUT_LENGTH=512

# Configuración de Redis
REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_TTL_HOURS=24
ENABLE_CACHE=true
```

### Configuración de Redis

1. Instalar Redis:
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS con Homebrew
brew install redis
```

2. Iniciar Redis:
```bash
redis-server
```

## Instalación con Docker

1. Construir la imagen:
```bash
docker build -t ocr-llm .
```

2. Ejecutar el contenedor:
```bash
docker run -p 8000:8000 \
  -e MODEL_NAME=naver-clova-ix/donut-base-finetuned-cord-v2 \
  -e USE_GPU=false \
  ocr-llm
```

## Verificación de la Instalación

1. Ejecutar las pruebas:
```bash
pytest
```

2. Iniciar la API:
```bash
uvicorn src.interfaces.api.app:app --reload
```

3. Verificar la instalación:
```bash
curl http://localhost:8000/health
```

## Solución de Problemas

### Problemas Comunes

1. Error de GPU no disponible:
   - Verifica que CUDA está instalado correctamente
   - Configura `USE_GPU=false` si no tienes GPU

2. Error de conexión a Redis:
   - Verifica que Redis está en ejecución
   - Comprueba la URL de conexión
   - Configura `ENABLE_CACHE=false` para deshabilitar el caché

3. Error de memoria:
   - Ajusta `MAX_OUTPUT_LENGTH` según tus necesidades
   - Considera usar procesamiento por lotes

## Actualización

Para actualizar a la última versión:

```bash
pip install --upgrade ocr-llm-cli
```

O desde el código fuente:

```bash
git pull
pip install -e ".[dev]"
```
