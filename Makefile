.PHONY: up down build logs process clean

# Iniciar servicios
up:
	mkdir -p pdfs output
	docker compose up -d --build

# Detener servicios
down:
	docker compose down

# Reconstruir servicios
build:
	docker compose build

# Ver logs
logs:
	docker compose logs -f

# Procesar un PDF específico
# Uso: make process PDF=nombre_archivo.pdf
process:
	@if [ -z "$(PDF)" ]; then \
		echo "Especifica el PDF a procesar: make process PDF=archivo.pdf"; \
		exit 1; \
	fi
	docker compose exec ocr python ocr_donut.py "pdfs/$(PDF)"

# Limpiar todo
clean:
	docker compose down --rmi all
	rm -rf output/*
