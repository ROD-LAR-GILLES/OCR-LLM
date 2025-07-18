# Documentación de la API

## Información General

- Base URL: `http://localhost:8000`
- Formato: JSON
- Autenticación: No requerida (por ahora)

## Endpoints

### Procesar un Documento

```http
POST /api/v1/documents
```

Procesa un único documento PDF y extrae su texto.

#### Parámetros de la Solicitud

| Nombre    | Tipo   | Requerido | Descripción                    |
|-----------|--------|-----------|--------------------------------|
| file      | File   | Sí        | Archivo PDF a procesar         |
| quality   | int    | No        | Calidad del OCR (1-100)       |
| language  | string | No        | Idioma del documento           |
| format    | string | No        | Formato de salida (text/json)  |

#### Ejemplo de Solicitud

```bash
curl -X POST http://localhost:8000/api/v1/documents \
  -F "file=@documento.pdf" \
  -F "quality=90" \
  -F "language=es" \
  -F "format=text"
```

#### Respuesta Exitosa

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "original_name": "documento.pdf",
  "text": "Contenido extraído del documento...",
  "processed_at": "2025-07-18T14:30:00Z",
  "processing_time": 2.5,
  "quality_score": 0.95,
  "page_count": 3,
  "word_count": 1500
}
```

### Procesar Múltiples Documentos

```http
POST /api/v1/documents/batch
```

Procesa múltiples documentos en un solo lote.

#### Parámetros de la Solicitud

| Nombre    | Tipo     | Requerido | Descripción                    |
|-----------|----------|-----------|--------------------------------|
| files     | File[]   | Sí        | Lista de archivos PDF         |
| quality   | int      | No        | Calidad del OCR (1-100)       |
| language  | string   | No        | Idioma de los documentos      |
| format    | string   | No        | Formato de salida (text/json)  |

#### Ejemplo de Solicitud

```bash
curl -X POST http://localhost:8000/api/v1/documents/batch \
  -F "files=@doc1.pdf" \
  -F "files=@doc2.pdf" \
  -F "quality=90"
```

#### Respuesta Exitosa

```json
{
  "batch_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_documents": 2,
  "processed_documents": 2,
  "failed_documents": 0,
  "started_at": "2025-07-18T14:30:00Z",
  "completed_at": "2025-07-18T14:31:00Z",
  "documents": [
    {
      "id": "doc1-id",
      "original_name": "doc1.pdf",
      "text": "Contenido del documento 1...",
      "processed_at": "2025-07-18T14:30:30Z",
      "processing_time": 1.5,
      "quality_score": 0.92,
      "page_count": 2,
      "word_count": 800
    },
    {
      "id": "doc2-id",
      "original_name": "doc2.pdf",
      "text": "Contenido del documento 2...",
      "processed_at": "2025-07-18T14:31:00Z",
      "processing_time": 1.8,
      "quality_score": 0.88,
      "page_count": 3,
      "word_count": 1200
    }
  ]
}
```

## Endpoints de Monitoreo

### Métricas Prometheus

```http
GET /metrics
```

Retorna métricas en formato Prometheus.

### Estado del Servicio

```http
GET /health
```

Retorna el estado actual del servicio.

#### Respuesta Exitosa

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": 3600,
  "components": {
    "redis": "connected",
    "model": "loaded"
  }
}
```

## Manejo de Errores

La API usa códigos de estado HTTP estándar y retorna errores en el siguiente formato:

```json
{
  "detail": "Descripción del error",
  "error_code": "ERROR_CODE",
  "timestamp": "2025-07-18T14:30:00Z",
  "path": "/api/v1/documents"
}
```

### Códigos de Error Comunes

| Código | Descripción                                |
|--------|-------------------------------------------|
| 400    | Solicitud inválida                        |
| 404    | Recurso no encontrado                     |
| 415    | Tipo de archivo no soportado              |
| 429    | Demasiadas solicitudes                    |
| 500    | Error interno del servidor                |

## Límites y Cuotas

- Tamaño máximo de archivo: 50MB
- Máximo de archivos por lote: 10
- Límite de solicitudes: 100 por minuto
- Tiempo máximo de procesamiento: 300 segundos
