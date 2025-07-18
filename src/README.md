# Estructura del Proyecto OCR-LLM

Este proyecto implementa una arquitectura hexagonal (puertos y adaptadores) para procesar documentos PDF mediante OCR y mejorar el texto utilizando modelos de lenguaje (LLM).

## Estructura de Carpetas

```
src/
├── config/        # Configuración y contenedor de dependencias
├── domain/        # Lógica de negocio, modelos y puertos
├── infrastructure/# Implementaciones concretas (adaptadores)
├── interfaces/    # Interfaces de usuario (CLI)
└── main.py        # Punto de entrada de la aplicación
```

## Flujo de la Aplicación

1. El usuario interactúa a través de la CLI (`interfaces/cli.py`)
2. Los comandos son procesados por casos de uso (`domain/use_cases.py`)
3. Los casos de uso utilizan puertos (`domain/ports.py`) para operaciones
4. Los adaptadores (`infrastructure/`) implementan los puertos
5. Los resultados se almacenan usando el adaptador de almacenamiento

## Configuración

El proyecto utiliza variables de entorno a través de un archivo `.env`. Las principales configuraciones son:

- `OPENAI_API_KEY`: Clave API de OpenAI
- `TESSERACT_PATH`: Ruta al ejecutable de Tesseract
- `OCR_LANG`: Idioma para OCR (default: "spa")
- `INPUT_DIR`: Directorio de entrada (default: "pdfs")
- `OUTPUT_DIR`: Directorio de salida (default: "output")

## Dependencias Principales

- `openai`: Cliente API de OpenAI
- `pytesseract`: OCR con Tesseract
- `pymupdf`: Procesamiento de PDFs
- `dependency-injector`: Inyección de dependencias
- `click`: Interface de línea de comandos
- `pydantic`: Validación de datos y configuración
