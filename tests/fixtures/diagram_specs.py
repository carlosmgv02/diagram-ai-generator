"""Test fixtures for diagram specifications"""

SIMPLE_AWS_SPEC = {
    "title": "Simple AWS Architecture",
    "provider": "aws",
    "layout": "horizontal",
    "components": [
        {
            "id": "web1",
            "type": "EC2",
            "category": "compute",
            "label": "Web Server"
        },
        {
            "id": "db1",
            "type": "RDS",
            "category": "database",
            "label": "Database"
        }
    ],
    "connections": [
        {
            "from": "web1",
            "to": "db1",
            "label": "queries"
        }
    ],
    "clusters": []
}

MULTICLOUD_SPEC = {
    "title": "Multi-Cloud Architecture",
    "provider": "aws",
    "layout": "vertical",
    "components": [
        {
            "id": "aws_web",
            "type": "EC2",
            "category": "compute",
            "label": "AWS Web",
            "component_provider": "aws"
        },
        {
            "id": "azure_db",
            "type": "SQLDatabases",
            "category": "database",
            "label": "Azure DB",
            "component_provider": "azure"
        },
        {
            "id": "gcp_storage",
            "type": "GCS",
            "category": "storage",
            "label": "GCP Storage",
            "component_provider": "gcp"
        }
    ],
    "connections": [
        {
            "from": "aws_web",
            "to": "azure_db",
            "label": "writes",
            "color": "blue"
        },
        {
            "from": "aws_web",
            "to": "gcp_storage",
            "label": "stores",
            "color": "green",
            "style": "dashed"
        }
    ],
    "clusters": []
}

CLUSTERED_SPEC = {
    "title": "Clustered Architecture",
    "provider": "aws",
    "layout": "horizontal",
    "components": [
        {
            "id": "web1",
            "type": "EC2",
            "category": "compute",
            "label": "Web 1"
        },
        {
            "id": "web2",
            "type": "EC2",
            "category": "compute",
            "label": "Web 2"
        },
        {
            "id": "lb",
            "type": "ELB",
            "category": "network",
            "label": "Load Balancer"
        },
        {
            "id": "db1",
            "type": "RDS",
            "category": "database",
            "label": "Primary DB"
        },
        {
            "id": "db2",
            "type": "RDS",
            "category": "database",
            "label": "Replica DB"
        }
    ],
    "connections": [
        {"from": "lb", "to": "web1"},
        {"from": "lb", "to": "web2"},
        {"from": "web1", "to": "db1"},
        {"from": "web2", "to": "db1"},
        {"from": "db1", "to": "db2", "label": "replication", "style": "dashed"}
    ],
    "clusters": [
        {
            "name": "Web Tier",
            "components": ["web1", "web2"]
        },
        {
            "name": "Database Tier",
            "components": ["db1", "db2"]
        }
    ]
}

INVALID_SPEC = {
    "title": "Invalid Spec",
    "provider": "aws",
    "components": [
        {
            "id": "invalid1",
            "type": "NonExistentNode",
            "category": "invalid_category"
        }
    ],
    "connections": [],
    "clusters": []
}

