# Diagram AI Generator 🚀

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](docker/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-purple.svg)](https://modelcontextprotocol.io)

Professional AI-powered architecture diagram generator with **multi-cloud support** and **MCP (Model Context Protocol) server** integration. Generate beautiful, accurate diagrams with provider-specific icons for AWS, Azure, GCP, Kubernetes, and more.

## ✨ Features

- 🎯 **Professional Diagrams**: Generate diagrams with real provider icons (AWS Lambda, Azure Functions, GCP Storage, etc.)
- 🌐 **Multi-Cloud Support**: Mix AWS, Azure, GCP, and other providers in a single diagram
- 🧠 **Smart Node Suggestions**: Automatic suggestions when component names don't match exactly
- 🔧 **MCP Server Integration**: Works seamlessly with Claude Desktop and other MCP clients
- 🐳 **Docker Ready**: One-command deployment with Docker Compose
- 📦 **PyPI Package**: Install easily with pip
- 🏗️ **Modular Architecture**: Clean, scalable, and maintainable codebase

## 🚀 Quick Start

### Option 1: Install from PyPI (Recommended)

```bash
# Install the package
pip install diagram-ai-generator

# Start the MCP server
diagram-ai-mcp

# Or use programmatically
python3 -c "
from src import DiagramService
service = DiagramService()
print('✅ Diagram AI Generator ready!')
"
```

### Option 2: Development Installation

```bash
# Clone the repository
git clone https://github.com/diagram-ai/diagram-ai-generator.git
cd diagram-ai-generator

# Install in development mode
pip install -e .

# Start the MCP server
python3 scripts/run_mcp_server.py
```

### Option 3: Docker (Containerized)

```bash
# Clone and run with Docker
git clone https://github.com/diagram-ai/diagram-ai-generator.git
cd diagram-ai-generator
./scripts/run_docker.sh
```

## 🛠️ Usage

### MCP Server Integration

The MCP server provides 5 professional tools for creating diagrams:

1. **`step1_list_providers`** - List all available providers (AWS, Azure, GCP, etc.)
2. **`step2_get_categories`** - Get categories for a specific provider
3. **`step3_get_nodes`** - Get exact node names for a category
4. **`create_diagram_from_json`** - Generate diagrams from JSON specifications
5. **`multicloud_helper`** - Guide for multi-cloud diagrams

### Recommended Workflow

```
1. step1_list_providers()
   ↓
2. step2_get_categories("aws")
   ↓  
3. step3_get_nodes("aws", "compute")
   ↓
4. create_diagram_from_json(spec)
```

### Example: Single-Cloud Diagram

```json
{
  "title": "AWS Serverless Architecture",
  "provider": "aws",
  "layout": "horizontal",
  "components": [
    {
      "id": "api_gateway",
      "type": "APIGateway",
      "category": "network",
      "label": "API Gateway"
    },
    {
      "id": "lambda",
      "type": "Lambda",
      "category": "compute", 
      "label": "Lambda Function"
    },
    {
      "id": "dynamodb",
      "type": "Dynamodb",
      "category": "database",
      "label": "DynamoDB"
    }
  ],
  "connections": [
    {
      "from": "api_gateway",
      "to": "lambda",
      "color": "darkgreen",
      "style": "bold",
      "label": "HTTP"
    }
  ]
}
```

### Example: Multi-Cloud Diagram with Specific Icons

```json
{
  "title": "Multi-Cloud Architecture",
  "provider": "generic",
  "layout": "horizontal", 
  "components": [
    {
      "id": "aws_lambda",
      "type": "Lambda",
      "category": "compute",
      "component_provider": "aws",
      "label": "AWS Lambda"
    },
    {
      "id": "azure_func",
      "type": "FunctionApps", 
      "category": "compute",
      "component_provider": "azure",
      "label": "Azure Functions"
    },
    {
      "id": "gcp_func",
      "type": "Functions",
      "category": "compute",
      "component_provider": "gcp", 
      "label": "GCP Functions"
    }
  ],
  "clusters": [
    {
      "name": "AWS Cloud",
      "components": ["aws_lambda"]
    },
    {
      "name": "Azure Cloud",
      "components": ["azure_func"] 
    },
    {
      "name": "GCP Cloud",
      "components": ["gcp_func"]
    }
  ]
}
```

## 🌐 Multi-Cloud Support

### Key Features:
- ✅ **Real Provider Icons**: Each component uses its actual provider icon
- ✅ **Mixed Architectures**: Combine AWS, Azure, GCP in one diagram  
- ✅ **Smart Clustering**: Automatic grouping by cloud provider
- ✅ **Cross-Cloud Connections**: Show inter-cloud communication

### Important Notes:
- Use `"provider": "generic"` for multi-cloud diagrams
- Add `"component_provider": "aws"` to each component
- Use exact node names from `step3_get_nodes()`

## 📦 Docker Deployment

### Development
```bash
cd docker
docker-compose up -d
```

### Production
```bash
# Build production image
docker build -f docker/Dockerfile -t diagram-ai-generator .

# Run with custom configuration
docker run -d \
  -p 8080:8080 \
  -v $(pwd)/generated_diagrams:/app/generated_diagrams \
  diagram-ai-generator
```

## 🔧 Configuration

### Environment Variables
- `PYTHONPATH`: Set to project root (auto-configured)
- `PYTHONUNBUFFERED`: Enable real-time logging (auto-configured)

### Output Directory
Generated diagrams are saved to `generated_diagrams/` by default.

## 🏗️ Architecture

```
src/
├── application/
│   ├── mcp/
│   │   ├── server_modular.py      # Main MCP server
│   │   └── tools/                 # Individual MCP tools
│   │       ├── providers_tool.py  # List providers
│   │       ├── categories_tool.py # Get categories  
│   │       ├── nodes_tool.py      # Get nodes
│   │       ├── diagram_tool.py    # Create diagrams
│   │       └── multicloud_tool.py # Multi-cloud helper
│   └── services/
│       └── diagram_service.py     # Core diagram logic
└── infrastructure/
    └── external/
        └── diagrams_structure.json # Provider/node mapping
```

## 🧠 Smart Features

### Automatic Node Suggestions
When you use incorrect node names, the system suggests alternatives:

```
⚠️  NODO NO ENCONTRADO: 'DynamoDB' en aws/database
💡 SUGERENCIAS: Dynamodb, DocumentdbMongodbCompatibility
✅ USANDO SUGERENCIA: 'Dynamodb' en lugar de 'DynamoDB'
```

### Common Name Corrections
- ❌ `DynamoDB` → ✅ `Dynamodb`
- ❌ `EventBridge` → ✅ `Eventbridge`  
- ❌ `S3` → ✅ `SimpleStorageServiceS3`
- ❌ `PubSub` → ✅ `Pubsub`

## 📋 Supported Providers

- **AWS** - 400+ services across 30+ categories
- **Azure** - 300+ services across 25+ categories  
- **GCP** - 200+ services across 15+ categories
- **Kubernetes** - 50+ resources across 10+ categories
- **OnPrem** - 200+ tools and services
- **And 14 more providers...**

## 🔍 Troubleshooting

### Common Issues

**1. MCP Server Not Starting**
```bash
# Check Python version
python3 --version  # Should be 3.9+

# Install MCP dependencies
pip install "mcp>=0.1.0"
```

**2. Graphviz Not Found**
```bash
# Ubuntu/Debian
sudo apt-get install graphviz graphviz-dev

# macOS  
brew install graphviz
```

**3. Generic Icons in Multi-Cloud**
- Use `"provider": "generic"` 
- Add `"component_provider": "aws"` to each component
- Follow the exact JSON format from examples

**4. Node Not Found Errors**
- Use `step3_get_nodes()` to get exact names
- Check the suggestions in console output
- Use `multicloud_helper()` for guidance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📚 **Documentation**: Check this README and `/docs` folder
- 🐛 **Issues**: [GitHub Issues](https://github.com/diagram-ai/diagram-ai-generator/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/diagram-ai/diagram-ai-generator/discussions)

## ⭐ Star History

If this project helps you, please consider giving it a star! ⭐

---

Made with ❤️ by the Diagram AI Generator Team