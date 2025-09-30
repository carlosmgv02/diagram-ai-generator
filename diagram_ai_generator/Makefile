# Makefile para Diagram AI Generator

.PHONY: help install dev test lint format clean run-demo run-mcp

help: ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependencias y configura el proyecto
	@echo "🚀 Instalando Diagram AI Generator..."
	./install.sh

dev: ## Configura entorno de desarrollo
	@echo "🔧 Configurando entorno de desarrollo..."
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	. venv/bin/activate && pip install -e .
	@echo "✅ Entorno de desarrollo listo"

test: ## Ejecuta tests
	@echo "🧪 Ejecutando tests..."
	pytest tests/ -v

test-coverage: ## Ejecuta tests con coverage
	@echo "📊 Ejecutando tests con coverage..."
	pytest tests/ --cov=diagram_ai_generator --cov-report=html --cov-report=term

lint: ## Ejecuta linting
	@echo "🔍 Ejecutando linting..."
	flake8 src/
	mypy src/

format: ## Formatea el código
	@echo "✨ Formateando código..."
	black src/ tests/
	isort src/ tests/

clean: ## Limpia archivos temporales
	@echo "🧹 Limpiando archivos temporales..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ htmlcov/ .coverage
	rm -rf diagrams_output/*.png diagrams_output/*.svg diagrams_output/*.pdf

run-demo: ## Ejecuta el demo
	@echo "🎨 Ejecutando demo..."
	python demo.py

run-mcp: ## Ejecuta el servidor MCP
	@echo "🛠️  Ejecutando servidor MCP..."
	python -m diagram_ai_generator.src.application.mcp.server

generate-example: ## Genera un diagrama de ejemplo
	@echo "📊 Generando diagrama de ejemplo..."
	diagram-ai generate "aplicación web con load balancer, servidores web y base de datos" --title "Ejemplo de Arquitectura"

list-providers: ## Lista proveedores disponibles
	@echo "📋 Listando proveedores..."
	diagram-ai list-providers

search-aws: ## Busca componentes de AWS
	@echo "🔍 Buscando componentes de AWS..."
	diagram-ai search "ec2" --provider aws

test-connection: ## Prueba conexión con OpenAI
	@echo "🔌 Probando conexión..."
	diagram-ai test-connection

build: ## Construye el paquete
	@echo "📦 Construyendo paquete..."
	python setup.py sdist bdist_wheel

install-local: ## Instala desde código local
	@echo "📥 Instalando desde código local..."
	pip install -e .

docker-build: ## Construye imagen Docker (futuro)
	@echo "🐳 Docker build no implementado aún"

docs: ## Genera documentación (futuro)
	@echo "📚 Generación de docs no implementada aún"

# Comandos de desarrollo rápido
quick-test: ## Test rápido sin coverage
	pytest tests/ -x -v

quick-lint: ## Lint solo archivos modificados
	@echo "⚡ Lint rápido..."
	black --check src/
	flake8 src/

setup-env: ## Configura variables de entorno para desarrollo
	@echo "⚙️  Configurando variables de entorno..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "📝 Archivo .env creado. Configura tu API key."; fi

# Comandos de utilidad
show-structure: ## Muestra estructura del proyecto
	@echo "📁 Estructura del proyecto:"
	tree -I '__pycache__|*.pyc|venv|.git|htmlcov|*.egg-info' .

check-deps: ## Verifica dependencias
	@echo "🔍 Verificando dependencias..."
	@command -v python3 >/dev/null 2>&1 || { echo "❌ Python3 no encontrado"; exit 1; }
	@command -v dot >/dev/null 2>&1 || { echo "❌ Graphviz no encontrado"; exit 1; }
	@echo "✅ Dependencias del sistema OK"

init: install setup-env ## Inicialización completa del proyecto
	@echo "🎉 Proyecto inicializado. Ejecuta 'make run-demo' para probar."