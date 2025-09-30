# 🎨 Diagram AI Generator

Una herramienta de línea de comandos que utiliza inteligencia artificial para generar diagramas de arquitectura a partir de descripciones en lenguaje natural.

## ✨ Características

- 🤖 **Generación con IA**: Utiliza OpenAI para interpretar descripciones y generar diagramas
- 🏗️ **Arquitectura Hexagonal**: Diseño modular y extensible
- 🌐 **Múltiples Proveedores**: Soporte para AWS, Azure, GCP, Kubernetes, On-Premise y más
- 📊 **Múltiples Formatos**: PNG, SVG, PDF y DOT
- 🔍 **Búsqueda de Nodos**: Encuentra componentes específicos fácilmente
- 🛠️ **Servidor MCP**: Integración con Model Context Protocol para herramientas avanzadas
- 💻 **CLI Intuitiva**: Interfaz de línea de comandos fácil de usar

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- Graphviz (para renderizado de diagramas)
- API Key de OpenAI

### Instalación con bun (recomendado)

```bash
# Clonar el repositorio
git clone <repository-url>
cd diagram_ai_generator

# Instalar dependencias
bun install

# O usando pip
pip install -r requirements.txt
```

### Configuración

1. Copia el archivo de ejemplo de configuración:
```bash
cp .env.example .env
```

2. Edita el archivo `.env` y añade tu API key de OpenAI:
```env
OPENAI_API_KEY=tu_api_key_aqui
```

### Instalación de Graphviz

#### Ubuntu/Debian
```bash
sudo apt-get install graphviz
```

#### macOS
```bash
brew install graphviz
```

#### Windows
Descarga e instala desde: https://graphviz.org/download/

## 📖 Uso

### Comando Básico

```bash
# Generar un diagrama simple
diagram-ai generate "arquitectura web con load balancer, EC2 y RDS en AWS"
```

### Opciones Avanzadas

```bash
# Especificar tipo de diagrama y formato
diagram-ai generate "microservicios en Kubernetes" --type k8s --format svg --output ./mi_diagrama.svg

# Con título personalizado
diagram-ai generate "sistema de monitoreo" --title "Sistema de Monitoreo Corporativo" --type onprem
```

### Explorar Proveedores

```bash
# Listar todos los proveedores disponibles
diagram-ai list-providers

# Ver detalles de un proveedor específico
diagram-ai list-providers --provider aws --detailed

# Buscar componentes específicos
diagram-ai search "database" --provider aws
diagram-ai search "load balancer"
```

### Probar Conexión

```bash
# Verificar que la conexión con OpenAI funciona
diagram-ai test-connection
```

## 🔧 Servidor MCP

El proyecto incluye un servidor MCP (Model Context Protocol) que proporciona herramientas para integración con sistemas de IA más avanzados.

### Ejecutar el Servidor MCP

```bash
# Ejecutar servidor MCP
python -m diagram_ai_generator.src.application.mcp.server
```

### Herramientas MCP Disponibles

- `list_all_providers()`: Lista todos los proveedores
- `get_provider_categories(provider_name)`: Obtiene categorías de un proveedor
- `search_nodes(query, provider_filter, limit)`: Busca nodos específicos
- `get_providers_summary()`: Resumen estadístico

### Recursos Dinámicos

- `provider://aws`: Información detallada del proveedor AWS
- `category://aws/compute`: Nodos de la categoría compute de AWS

## 🏗️ Arquitectura

El proyecto sigue una arquitectura hexagonal (puertos y adaptadores):

```
src/
├── domain/                 # Lógica de negocio
│   ├── entities/          # Entidades del dominio
│   ├── repositories/      # Interfaces de repositorios
│   └── use_cases/         # Casos de uso
├── infrastructure/        # Implementaciones externas
│   ├── adapters/         # Adaptadores (OpenAI, Diagrams)
│   └── external/         # Datos externos
└── application/          # Interfaces de aplicación
    ├── cli/             # Interfaz de línea de comandos
    └── mcp/             # Servidor MCP
```

## 📊 Proveedores Soportados

| Proveedor | Nodos | Categorías | Descripción |
|-----------|-------|------------|-------------|
| AWS | 500+ | 25+ | Amazon Web Services |
| Azure | 229+ | 16+ | Microsoft Azure |
| GCP | 93+ | 12+ | Google Cloud Platform |
| Kubernetes | 45+ | 12+ | Orquestación de contenedores |
| On-Premise | 172+ | 31+ | Infraestructura local |
| Generic | 26+ | 9+ | Componentes genéricos |
| Programming | 73+ | 4+ | Lenguajes y frameworks |

## 🎯 Ejemplos de Uso

### Arquitectura Web AWS
```bash
diagram-ai generate "aplicación web con ALB, EC2 en múltiples AZ, RDS con réplica de lectura y CloudFront"
```

### Microservicios en Kubernetes
```bash
diagram-ai generate "arquitectura de microservicios con API Gateway, servicios en pods, Redis para caché y PostgreSQL"
```

### Infraestructura On-Premise
```bash
diagram-ai generate "datacenter con servidores web, balanceador HAProxy, cluster de base de datos y sistema de monitoreo"
```

## 🛠️ Desarrollo

### Estructura del Proyecto

```bash
# Ejecutar tests
pytest tests/

# Formatear código
black src/
isort src/

# Análisis estático
mypy src/
flake8 src/
```

### Agregar Nuevos Proveedores

1. Actualizar `diagrams_structure.json` con los nuevos nodos
2. Implementar adaptador en `infrastructure/adapters/`
3. Actualizar casos de uso si es necesario

### Extender Funcionalidad

La arquitectura hexagonal permite fácil extensión:
- Nuevos proveedores de IA (Anthropic, Cohere, etc.)
- Nuevos formatos de salida
- Nuevas interfaces (Web, API REST)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🐛 Reportar Problemas

Si encuentras algún problema o tienes sugerencias, por favor abre un issue en GitHub.

## 📚 Referencias

- [Diagrams Library](https://diagrams.mingrammer.com/)
- [OpenAI API](https://platform.openai.com/docs)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Click Documentation](https://click.palletsprojects.com/)

---

Hecho con ❤️ y ☕ para la comunidad de desarrolladores.