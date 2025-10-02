# Diagram AI Generator 🚀

[![PyPI version](https://img.shields.io/pypi/v/diagram-ai-generator.svg)](https://pypi.org/project/diagram-ai-generator/)
[![Python](https://img.shields.io/pypi/pyversions/diagram-ai-generator.svg)](https://pypi.org/project/diagram-ai-generator/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/diagram-ai-generator.svg)](https://pypi.org/project/diagram-ai-generator/)

[![PR Checks](https://github.com/carlosmgv02/diagram-ai-generator/actions/workflows/pr-check.yml/badge.svg)](https://github.com/carlosmgv02/diagram-ai-generator/actions/workflows/pr-check.yml)
[![Release](https://github.com/carlosmgv02/diagram-ai-generator/actions/workflows/release.yml/badge.svg)](https://github.com/carlosmgv02/diagram-ai-generator/actions/workflows/release.yml)
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

## 📸 Example Output

Here's a real diagram generated with a simple text prompt:

**Prompt**: *"aplicación web en AWS con ALB, EC2 en múltiples zonas de disponibilidad, RDS con réplica de lectura, ElastiCache para caché y CloudFront para CDN y muchas mas cosas con layout horizontal para que se vea completo y bien"*

![AWS High Availability Architecture](https://github.com/carlosmgv02/diagram-ai-generator/blob/master/assets/example_aws_architecture.png)

**Generated in seconds** with professional AWS icons, proper layout, and accurate cloud architecture patterns! 🎉

### ⚡ How It Works

Simply describe your architecture in plain text:
- ✅ "Create a microservices architecture with load balancer, containers, and Redis cache"
- ✅ "Design a data pipeline with S3, Lambda, and Kinesis"
- ✅ "Build a multi-region setup with CloudFront, ALB, and RDS"

The AI understands your requirements and generates **production-ready** diagrams with the correct cloud provider icons and relationships.

## 🚀 Quick Start

### Step 1: Install the package

```bash
pip install diagram-ai-generator
```

**Note:** Use your system Python (the one Claude Desktop uses):
```bash
# macOS
/usr/local/bin/python3 -m pip install diagram-ai-generator

# Or force install from PyPI
pip install diagram-ai-generator
```

### Step 2: Configure Claude Desktop

That's it! Now configure it in Claude Desktop (see next section).

## 🔌 Claude Desktop Configuration

Edit your `claude_desktop_config.json`:

**Location:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Basic Configuration:**

```json
{
    "mcpServers": {
        "diagram-ai-generator": {
            "command": "python3",
            "args": ["-m", "src.application.mcp.server_modular"]
        }
    }
}
```

**With Custom Output Directory (Optional):**

```json
{
    "mcpServers": {
        "diagram-ai-generator": {
            "command": "python3",
            "args": ["-m", "src.application.mcp.server_modular"],
            "env": {
                "DIAGRAM_OUTPUT_DIR": "/Users/yourname/diagrams"
            }
        }
    }
}
```

The output directory will be created automatically if it doesn't exist. If not specified, diagrams are saved to `./generated_diagrams/` in your current directory.

**After configuration:**
1. Restart Claude Desktop
2. Start using it! Ask Claude to create architecture diagrams

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

### 💡 Real-World Examples

#### Example 1: AWS Serverless E-commerce

**Simple prompt**: "Create a serverless e-commerce backend on AWS with API Gateway, Lambda functions, DynamoDB, and S3 for product images"

**What you get**:
- Professional AWS architecture diagram
- Correct service icons and relationships
- Production-ready layout

#### Example 2: Multi-Cloud Disaster Recovery

**Simple prompt**: "Multi-cloud setup with primary services in AWS and failover in Azure"

**What you get**:
- Clear separation between cloud providers
- Cross-cloud connections
- Both AWS and Azure specific icons

#### Example 3: Kubernetes Microservices

**Simple prompt**: "Kubernetes cluster with microservices, ingress controller, and persistent storage"

**What you get**:
- Kubernetes-specific resources
- Proper namespace organization
- Service mesh visualization

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

## ⚙️ Configuration Options

### Output Directory

By default, diagrams are saved to `./generated_diagrams/`. You can customize this:

```json
{
    "mcpServers": {
        "diagram-ai-generator": {
            "command": "python3",
            "args": ["-m", "src.application.mcp.server_modular"],
            "env": {
                "DIAGRAM_OUTPUT_DIR": "/path/to/your/diagrams"
            }
        }
    }
}
```

The directory will be created automatically if it doesn't exist.

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

**1. Module not found error**
Make sure you have Python 3.10+ and installed in the correct Python:
```bash
# Check Python version
python3 --version  # Should be 3.10 or higher

# Install
/usr/local/bin/python3 -m pip install diagram-ai-generator
```

**2. Graphviz not found**
```bash
# macOS  
brew install graphviz

# Ubuntu/Debian
sudo apt-get install graphviz
```

**3. Custom output directory not working**
- Make sure the path exists or the directory is writable
- Use absolute paths in the configuration
- Check Claude Desktop logs for errors

## 🔧 Development

### Contributing

1. Fork the repository
2. Create a feature branch from `develop`
3. Make your changes
4. Open a PR to `develop`

### Release Process

**Automated with GitHub Actions:**

1. **PR to master**: Triggers checks
   - Tests and build validation
   - Analyzes changes (code vs docs only)
   - Comments on PR if release will be created

2. **Merge to master**: Auto-deploys if version changed
   - Builds package
   - Publishes to PyPI
   - Creates GitHub release
   - Updates CHANGELOG

### Versioning

Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` - New feature (bumps MINOR version)
- `fix:` - Bug fix (bumps PATCH version)  
- `BREAKING CHANGE:` - Breaking change (bumps MAJOR version)
- `docs:` - Documentation only (no release)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/carlosmgv02/diagram-ai-generator/issues)
- 📝 **Changelog**: [CHANGELOG.md](CHANGELOG.md)

---

Made by [Carlos Martínez García-Villarrubia](https://github.com/carlosmgv02)
