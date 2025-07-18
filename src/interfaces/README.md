# Capa de Interfaces

Esta carpeta contiene las interfaces de usuario del proyecto, actualmente implementando una interfaz de línea de comandos (CLI).

## Archivos

### `cli.py`

Implementa la interfaz de línea de comandos usando Click.

```python
@click.group()
def cli():
    """OCR-LLM CLI - Procesa documentos PDF con OCR y mejora con LLM"""
    pass

@cli.command()
@click.argument('pdf_path')
@click.option('--output-format', '-f', default='markdown')
@click.option('--batch-size', '-b', default=5)
def process(pdf_path: str, output_format: str, batch_size: int):
    """Procesa un documento PDF"""
    # Implementación del comando
```

## Comandos Disponibles

### Procesar Documento
```bash
ocr-llm process path/to/document.pdf --output-format markdown
```

Opciones:
- `--output-format, -f`: Formato de salida (markdown/text/json)
- `--batch-size, -b`: Tamaño del batch para procesamiento LLM

### Listar Documentos
```bash
ocr-llm list
```

Muestra los documentos procesados en el directorio de salida.

### Configuración
```bash
ocr-llm config show
ocr-llm config set key value
```

Gestiona la configuración del proyecto.

## Ejemplos de Uso

```bash
# Procesar un documento
ocr-llm process docs/ejemplo.pdf -f markdown

# Procesar múltiples documentos
ocr-llm process docs/*.pdf --batch-size 10

# Ver configuración actual
ocr-llm config show

# Cambiar modelo de LLM
ocr-llm config set llm_model gpt-4
```

## Manejo de Errores

La CLI implementa manejo de errores para:
- Archivos no encontrados
- Errores de OCR
- Errores de API de OpenAI
- Problemas de almacenamiento

Cada error muestra un mensaje descriptivo y, cuando es relevante, sugerencias de solución.
