# Ejemplos de Uso

Esta guía proporciona ejemplos prácticos de cómo usar Diagram AI Generator para crear diferentes tipos de diagramas de arquitectura.

## 🚀 Ejemplos Básicos

### Arquitectura Web Simple

```bash
diagram-ai generate "aplicación web con servidor web, base de datos y balanceador de carga"
```

**Resultado esperado**: Diagrama con componentes web básicos conectados lógicamente.

### Microservicios en la Nube

```bash
diagram-ai generate "arquitectura de microservicios con API Gateway, 3 servicios y base de datos compartida" --type aws
```

## ☁️ Arquitecturas Cloud

### AWS - Aplicación Web Escalable

```bash
diagram-ai generate "aplicación web en AWS con ALB, EC2 en múltiples zonas de disponibilidad, RDS con réplica de lectura, ElastiCache para caché y CloudFront para CDN" --type aws --format svg
```

**Componentes esperados**:
- Application Load Balancer (ALB)
- EC2 instances en múltiples AZ
- RDS con read replica
- ElastiCache
- CloudFront

### Azure - Plataforma de Datos

```bash
diagram-ai generate "plataforma de análisis de datos en Azure con Data Factory, Azure SQL, Databricks y Power BI" --type azure --title "Plataforma de Analytics"
```

### Google Cloud - ML Pipeline

```bash
diagram-ai generate "pipeline de machine learning en GCP con Cloud Storage, Dataflow, BigQuery, AI Platform y Cloud Functions" --type gcp
```

## 🐳 Kubernetes y Contenedores

### Aplicación Containerizada

```bash
diagram-ai generate "aplicación en Kubernetes con ingress controller, servicios, pods, persistent volumes y secrets" --type k8s
```

### Microservicios con Service Mesh

```bash
diagram-ai generate "microservicios en Kubernetes con Istio service mesh, múltiples namespaces y observabilidad" --type k8s --format pdf
```

## 🏢 Infraestructura On-Premise

### Datacenter Tradicional

```bash
diagram-ai generate "datacenter con servidores web en cluster, balanceador HAProxy, base de datos PostgreSQL en alta disponibilidad y sistema de monitoreo Prometheus" --type onprem
```

### Arquitectura de Red Empresarial

```bash
diagram-ai generate "red empresarial con firewall perimetral, DMZ, servidores internos, Active Directory y backup system" --type onprem
```

## 🔧 Ejemplos Específicos por Dominio

### E-commerce

```bash
diagram-ai generate "plataforma de e-commerce con frontend React, API Gateway, microservicios de productos, usuarios, pedidos y pagos, Redis para sesiones, PostgreSQL para datos y Elasticsearch para búsquedas"
```

### Sistema de Monitoreo

```bash
diagram-ai generate "sistema de monitoreo con Prometheus para métricas, Grafana para dashboards, AlertManager para alertas, Elasticsearch para logs y Jaeger para tracing"
```

### CI/CD Pipeline

```bash
diagram-ai generate "pipeline CI/CD con GitLab, Jenkins, SonarQube para calidad, Artifactory para artefactos, Kubernetes para despliegue y Prometheus para monitoreo" --type programming
```

### Sistema de Streaming

```bash
diagram-ai generate "arquitectura de streaming de datos con Apache Kafka, Apache Spark, Apache Flink, ClickHouse para analytics y Grafana para visualización"
```

## 🎯 Casos de Uso Avanzados

### Multi-Cloud

```bash
diagram-ai generate "arquitectura multi-cloud con AWS para compute, Azure para analytics, GCP para ML, conectados via VPN y con gestión centralizada"
```

### Edge Computing

```bash
diagram-ai generate "arquitectura edge computing con dispositivos IoT, edge gateways, procesamiento local, sincronización con cloud y analytics centralizados"
```

### Disaster Recovery

```bash
diagram-ai generate "arquitectura de disaster recovery con sitio principal, sitio de respaldo, replicación de datos, balanceadores de carga y failover automático"
```

## 🔍 Exploración de Componentes

### Buscar Componentes Específicos

```bash
# Buscar componentes de base de datos
diagram-ai search "database" --provider aws

# Buscar balanceadores de carga
diagram-ai search "load balancer"

# Buscar componentes de red en Azure
diagram-ai search "network" --provider azure
```

### Explorar Proveedores

```bash
# Ver todos los proveedores disponibles
diagram-ai list-providers

# Ver detalles de AWS
diagram-ai list-providers --provider aws --detailed

# Ver categorías de Kubernetes
diagram-ai list-providers --provider k8s
```

## 📊 Formatos de Salida

### PNG (Default)
```bash
diagram-ai generate "arquitectura simple" --format png
```

### SVG (Vectorial)
```bash
diagram-ai generate "arquitectura compleja" --format svg --output ./diagramas/arquitectura.svg
```

### PDF (Documentación)
```bash
diagram-ai generate "arquitectura empresarial" --format pdf --title "Arquitectura Empresarial 2024"
```

### DOT (Graphviz)
```bash
diagram-ai generate "diagrama de red" --format dot
```

## 🛠️ Configuración Avanzada

### Variables de Entorno

```bash
# Configurar modelo específico
export OPENAI_MODEL=gpt-4o-mini

# Configurar directorio de salida
export DEFAULT_OUTPUT_DIR=./mis_diagramas

# Habilitar debug
export DEBUG=true
```

### Archivos de Configuración

Crear `.env` personalizado:
```env
OPENAI_API_KEY=sk-tu-key-aqui
OPENAI_MODEL=gpt-4o
DEFAULT_OUTPUT_DIR=./output
DEFAULT_FORMAT=svg
DEBUG=false
LOG_LEVEL=INFO
```

## 🎨 Tips para Mejores Resultados

### 1. Sé Específico en las Descripciones

**❌ Malo**:
```bash
diagram-ai generate "sistema web"
```

**✅ Bueno**:
```bash
diagram-ai generate "aplicación web de e-commerce con React frontend, Node.js API, PostgreSQL database, Redis cache, y nginx load balancer"
```

### 2. Menciona Tecnologías Específicas

**✅ Incluye tecnologías**:
```bash
diagram-ai generate "microservicios con Spring Boot, Apache Kafka para mensajería, PostgreSQL para datos, Redis para caché, y deployment en Kubernetes"
```

### 3. Especifica Patrones Arquitectónicos

**✅ Menciona patrones**:
```bash
diagram-ai generate "arquitectura hexagonal con API Gateway, CQRS pattern, Event Sourcing con Kafka, y microservicios independientes"
```

### 4. Incluye Aspectos No Funcionales

**✅ Incluye NFRs**:
```bash
diagram-ai generate "sistema de alta disponibilidad con load balancers redundantes, base de datos en cluster, monitoring con Prometheus, y backup automático"
```

## 🔧 Servidor MCP - Ejemplos Avanzados

### Ejecutar Servidor MCP

```bash
python -m diagram_ai_generator.src.application.mcp.server
```

### Herramientas MCP Disponibles

```python
# Listar todos los proveedores
list_all_providers()

# Obtener categorías de AWS
get_provider_categories("aws")

# Buscar nodos específicos
search_nodes("database", provider_filter="aws", limit=10)

# Obtener resumen estadístico
get_providers_summary()
```

### Recursos Dinámicos MCP

```
# Información detallada de AWS
provider://aws

# Categoría compute de AWS
category://aws/compute

# Categoría network de Azure
category://azure/network
```

## 🐛 Solución de Problemas

### Error: "OpenAI API key is required"
```bash
export OPENAI_API_KEY=tu-key-aqui
# O crear archivo .env
```

### Error: "Graphviz not found"
```bash
# Ubuntu/Debian
sudo apt-get install graphviz

# macOS
brew install graphviz
```

### Diagrama vacío o incompleto
- Verifica que la descripción sea específica
- Intenta con un tipo de proveedor específico
- Revisa que los componentes mencionados existan

### Conexión lenta o timeouts
```bash
# Probar conexión
diagram-ai test-connection

# Usar modelo más rápido
export OPENAI_MODEL=gpt-4o-mini
```

## 📈 Casos de Uso por Industria

### Fintech
```bash
diagram-ai generate "plataforma fintech con API de pagos, microservicio de KYC, base de datos encriptada, audit logs, y compliance monitoring"
```

### Healthcare
```bash
diagram-ai generate "sistema de salud con FHIR API, base de datos HIPAA compliant, sistema de citas, EMR integration, y analytics de pacientes"
```

### Gaming
```bash
diagram-ai generate "arquitectura de juego online con game servers, matchmaking service, leaderboards, chat system, y CDN para assets"
```

### IoT
```bash
diagram-ai generate "plataforma IoT con device management, MQTT broker, time series database, real-time analytics, y dashboard de monitoreo"
```

---

¿Tienes un caso de uso específico? ¡Abre un issue en GitHub y lo agregaremos a los ejemplos!
