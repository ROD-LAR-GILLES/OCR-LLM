import click
from dependency_injector.wiring import inject, Provide
from config.container import Container
from domain.use_cases import DocumentProcessor, ProcessDocumentRequest

@click.command()
@click.argument('pdf_path')
@click.option('--output-format', '-f', default='markdown', 
              type=click.Choice(['markdown', 'text', 'json']))
@click.option('--batch-size', '-b', default=5, help='Batch size for LLM processing')
@inject
def process_document(
    pdf_path: str,
    output_format: str,
    batch_size: int,
    processor: DocumentProcessor = Provide[Container.document_processor]
):
    """Procesa un documento PDF usando OCR y refinamiento con LLM"""
    try:
        request = ProcessDocumentRequest(
            pdf_path=pdf_path,
            output_format=output_format,
            batch_size=batch_size
        )
        result = processor.process_document(request)
        click.echo(f"Documento procesado exitosamente: {result.name}")
        
    except Exception as e:
        click.echo(f"Error procesando documento: {str(e)}", err=True)
        raise click.Abort()