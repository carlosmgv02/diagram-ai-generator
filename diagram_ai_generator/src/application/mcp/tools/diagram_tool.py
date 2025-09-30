import json
from typing import Optional, Dict, Any
from src.application.mcp.tools.base_tool import BaseTool, register_tool

class DiagramTool(BaseTool):
    @register_tool
    def create_diagram_from_json(
        self,
        diagram_spec: str,
        title: Optional[str] = None
    ) -> str:
        """
        🔥 HERRAMIENTA PRINCIPAL: Crea un diagrama de arquitectura a partir de una especificación JSON.
        
        💡 FLUJO RECOMENDADO PARA ICONOS PROFESIONALES:
        1. step1_list_providers() → Ver todos los proveedores disponibles
        2. step2_get_categories("aws") → Ver categorías del proveedor elegido  
        3. step3_get_nodes("aws", "compute") → Ver nodos exactos de la categoría
        4. create_diagram_from_json() → Crear diagrama con nombres exactos obtenidos
        
        ⚠️ Usar nombres exactos de los pasos anteriores garantiza iconos correctos
        
        Args:
            diagram_spec: Especificación JSON del diagrama. FORMATO EXACTO REQUERIDO:
            
            IMPORTANTE: 
            - NO uses "children" - USA "clusters" 
            - NO uses "Group" - USA los tipos correctos
            - SIEMPRE incluye colores y estilos en las conexiones
            
            {
                "title": "Advanced Web Service with Monitoring",
                "provider": "onprem", 
                "layout": "vertical",
                "components": [
                    {
                        "id": "nginx",
                        "type": "Nginx",
                        "category": "network", 
                        "label": "ingress"
                    }
                ],
                "connections": [
                    {
                        "from": "nginx", 
                        "to": "server1",
                        "color": "darkgreen",
                        "style": "bold",
                        "label": "HTTP"
                    }
                ],
                "clusters": [
                    {
                        "name": "Service Cluster",
                        "components": ["server1", "server2", "server3"]
                    }
                ]
            }
            
            IMPORTANTE PARA MULTI-CLOUD CON ICONOS ESPECÍFICOS:
            - Para diagramas SINGLE-CLOUD: usar "provider": "aws", "azure", "gcp", etc.
            - Para diagramas MULTI-CLOUD: usar "component_provider" en cada componente
            
            EJEMPLO MULTI-CLOUD CON ICONOS ESPECÍFICOS:
            {
              "provider": "generic",
              "components": [
                {
                  "id": "lambda",
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
              ]
            }
            
            title: Título opcional para el diagrama
        
        Returns:
            Información del diagrama generado con imagen en base64
        """
        try:
            # Parsear la especificación JSON
            spec = json.loads(diagram_spec)
            
            # Agregar título si se proporciona
            if title:
                spec['title'] = title
            
            # Generar el diagrama
            result = self.diagram_service.create_diagram_from_spec(spec)
            
            if result['success']:
                response = f"""✅ Diagrama creado exitosamente!

📊 **Detalles:**
- Título: {result['title']}
- Proveedor: {result['provider']}
- Componentes: {result['components_count']}
- Conexiones: {result['connections_count']}
- Tamaño: {result['image_size_mb']} MB

📁 **Archivo guardado en:** `{result['file_path']}`

Para abrir el archivo: `open "{result['file_path']}"`

🖼️ **Imagen guardada localmente** (usar el comando 'open' de arriba para visualizar)"""
                
                return response
            else:
                return f"❌ Error: {result['error']}"
                
        except json.JSONDecodeError as e:
            return f"❌ Error: JSON inválido - {str(e)}"
        except Exception as e:
            return f"❌ Error generando diagrama: {str(e)}"