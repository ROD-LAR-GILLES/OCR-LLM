.PHONY: dev-up dev-down test build clean logs shell setup quality

# Development environment
dev-up:
	@echo "🚀 Starting development environment..."
	docker-compose -f docker-compose.dev.yml up -d

dev-down:
	@echo "🛑 Stopping development environment..."
	docker-compose -f docker-compose.dev.yml down

# Testing and quality
test:
	@echo "🧪 Running tests..."
	docker-compose -f docker-compose.dev.yml exec app pytest tests/ -v

test-coverage:
	@echo "📊 Running tests with coverage..."
	docker-compose -f docker-compose.dev.yml exec app pytest tests/ --cov=src --cov-report=html

quality:
	@echo "🔍 Running code quality checks..."
	docker-compose -f docker-compose.dev.yml exec app black --check src tests
	docker-compose -f docker-compose.dev.yml exec app isort --check-only src tests
	docker-compose -f docker-compose.dev.yml exec app flake8 src tests

# Building and deployment
build:
	@echo "🏗️ Building application..."
	docker build -t ocr-llm:latest .

# Utilities
logs:
	@echo "📝 Showing application logs..."
	docker-compose -f docker-compose.dev.yml logs -f app

shell:
	@echo "🐚 Opening application shell..."
	docker-compose -f docker-compose.dev.yml exec app /bin/bash

clean:
	@echo "🧹 Cleaning up..."
	docker-compose -f docker-compose.dev.yml down -v
	docker system prune -f

# Document processing
process:
	@if [ -z "$(PDF)" ]; then \
		echo "❌ Error: Especifica el PDF a procesar: make process PDF=archivo.pdf"; \
		exit 1; \
	fi
	@echo "📄 Processing $(PDF)..."
	docker-compose -f docker-compose.dev.yml exec app python -m src.interfaces.cli $(PDF)

# Setup and configuration
setup:
	@echo "⚙️ Setting up project..."
	@mkdir -p pdfs output logs monitoring/grafana/dashboards redis
	@cp .env.example .env || echo "⚠️ Configure .env manually"
	@echo "✅ Setup complete!"

# Health checks
health:
	@echo "🏥 Checking service health..."
	@curl -f http://localhost:8000/health || echo "❌ App health check failed"
	@redis-cli -h localhost ping || echo "❌ Redis health check failed"

jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"
      - "14268:14268"
    environment:
      - COLLECTOR_OTLP_ENABLED=true
    networks:
      - ocr-network
