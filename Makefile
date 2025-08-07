.PHONY: dev-up dev-down test build clean logs shell
.PHONY: up down build logs process clean
dev-up:
	@echo "Starting development environment..."niciar servicios
	docker-compose -f docker-compose.dev.yml up -d

dev-down:	docker compose up -d --build
	@echo "Stopping development environment..."
	docker-compose -f docker-compose.dev.yml downener servicios

test:	docker compose down
	@echo "Running tests..."
	docker-compose -f docker-compose.dev.yml exec app pytest tests/nstruir servicios

build:	docker compose build
	@echo "Building application..."
	docker build -t ocr-llm:latest . logs

clean:	docker compose logs -f
	@echo "Cleaning up..."
	docker-compose -f docker-compose.dev.yml down -v
	docker system prune -fake process PDF=nombre_archivo.pdf

logs:
	docker-compose -f docker-compose.dev.yml logs -f appecifica el PDF a procesar: make process PDF=archivo.pdf"; \
xit 1; \
shell:
	docker-compose -f docker-compose.dev.yml exec app /bin/bash	docker compose exec ocr python ocr_donut.py "pdfs/$(PDF)"

jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"
      - "14268:14268"
    environment:
      - COLLECTOR_OTLP_ENABLED=true
    networks:
      - ocr-network
