"""Constants and examples for MCP tools"""

# Language instruction for all tools
LANGUAGE_INSTRUCTION = """
IMPORTANT: Respond in the same language as the user's request.
If the user speaks Spanish, respond in Spanish.
If the user speaks English, respond in English.
"""

# Example diagram specifications
SINGLE_CLOUD_EXAMPLE = {
    "title": "Web Service Architecture",
    "provider": "aws",
    "layout": "vertical",
    "components": [
        {
            "id": "lb",
            "type": "ELB",
            "category": "network",
            "label": "Load Balancer"
        },
        {
            "id": "web1",
            "type": "EC2",
            "category": "compute",
            "label": "Web Server"
        },
        {
            "id": "db",
            "type": "RDS",
            "category": "database",
            "label": "Database"
        }
    ],
    "connections": [
        {
            "from": "lb",
            "to": "web1",
            "label": "routes",
            "color": "darkgreen"
        },
        {
            "from": "web1",
            "to": "db",
            "label": "queries",
            "style": "dashed"
        }
    ],
    "clusters": [
        {
            "name": "Application Tier",
            "components": ["lb", "web1"]
        }
    ]
}

MULTI_CLOUD_EXAMPLE = {
    "title": "Multi-Cloud Serverless",
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
            "label": "Cloud Functions"
        }
    ],
    "connections": [
        {
            "from": "aws_lambda",
            "to": "azure_func",
            "label": "event bridge"
        }
    ],
    "clusters": []
}

# Workflow recommendations
RECOMMENDED_WORKFLOW = """
📋 Recommended workflow for professional diagrams with correct icons:

1. list_providers() → See all available cloud providers
2. get_provider_categories(provider) → See categories for chosen provider
3. get_category_nodes(provider, category) → Get exact node names
4. create_diagram_from_json() → Create diagram with exact names from step 3

⚠️  Using exact names from the discovery steps ensures correct icons!
"""

# Connection styling options
CONNECTION_STYLES = {
    "colors": ["black", "blue", "red", "green", "darkgreen", "orange", "purple"],
    "styles": ["solid", "dashed", "dotted", "bold"],
    "labels": "Any descriptive text"
}

# Layout options
LAYOUT_OPTIONS = ["horizontal", "vertical"]

# Common providers
COMMON_PROVIDERS = ["aws", "azure", "gcp", "k8s", "onprem", "generic"]

