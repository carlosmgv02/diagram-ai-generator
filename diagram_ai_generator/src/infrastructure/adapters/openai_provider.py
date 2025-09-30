"""
Adaptador para OpenAI como proveedor de IA
"""
import json
import os
from typing import Optional

from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from ...domain.entities.diagram import DiagramRequest, DiagramSpec, DiagramNode, DiagramConnection, DiagramType
from ...domain.repositories.ai_provider_repository import AIProviderRepository
from ...domain.exceptions import AIProviderError


class DiagramSpecSchema(BaseModel):
    """Schema de Pydantic para la respuesta estructurada de OpenAI"""
    title: str = Field(description="Título del diagrama")
    description: str = Field(description="Descripción del diagrama")
    diagram_type: str = Field(description="Tipo de diagrama (aws, azure, gcp, etc.)")
    nodes: list[dict] = Field(description="Lista de nodos del diagrama")
    connections: list[dict] = Field(description="Lista de conexiones entre nodos")
    layout: Optional[str] = Field(default=None, description="Tipo de layout del diagrama")
    metadata: dict = Field(default_factory=dict, description="Metadatos adicionales")


class OpenAIProvider(AIProviderRepository):
    """Implementación del proveedor de IA usando OpenAI"""
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        model: str = "gpt-4o",
        base_url: Optional[str] = None,
        organization: Optional[str] = None
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self.organization = organization or os.getenv("OPENAI_ORG_ID")
        
        if not self.api_key:
            raise AIProviderError("OpenAI API key is required")
        
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            organization=self.organization
        )
        
        # Cargar información de proveedores disponibles
        self._load_providers_info()
    
    def _load_providers_info(self):
        """Carga la información de proveedores desde el archivo JSON"""
        try:
            providers_file = os.path.join(
                os.path.dirname(__file__), 
                "..", 
                "external", 
                "diagrams_structure.json"
            )
            with open(providers_file, 'r', encoding='utf-8') as f:
                self.providers_data = json.load(f)
        except FileNotFoundError:
            self.providers_data = {}
    
    def _create_system_prompt(self) -> str:
        """Crea el prompt del sistema con información sobre los proveedores disponibles"""
        
        providers_summary = []
        for provider, categories in self.providers_data.items():
            total_nodes = sum(len(nodes) for nodes in categories.values())
            providers_summary.append(f"- {provider.upper()}: {total_nodes} nodos en categorías {list(categories.keys())}")
        
        return f"""Eres un experto en arquitectura de sistemas y diagramas técnicos. Tu tarea es generar especificaciones de diagramas basadas en prompts del usuario.

PROVEEDORES DISPONIBLES:
{chr(10).join(providers_summary)}

INSTRUCCIONES:
1. Analiza el prompt del usuario para identificar:
   - Tipo de arquitectura (cloud provider, on-premise, etc.)
   - Componentes mencionados
   - Relaciones entre componentes

2. Selecciona el proveedor más apropiado basado en el contexto.

3. Genera una especificación JSON con:
   - title: Título descriptivo del diagrama
   - description: Descripción detallada de la arquitectura
   - diagram_type: Tipo de proveedor (aws, azure, gcp, k8s, onprem, generic, etc.)
   - nodes: Lista de nodos con name, node_type, provider, category, properties
   - connections: Lista de conexiones con source, target, label (opcional)
   - layout: Sugerencia de layout (opcional)
   - metadata: Información adicional

4. Para los nodos, usa nombres de componentes reales del proveedor seleccionado.

5. Las conexiones deben usar los nombres exactos de los nodos definidos.

EJEMPLO DE RESPUESTA:
{{
  "title": "Arquitectura Web AWS",
  "description": "Arquitectura web escalable en AWS con balanceador de carga",
  "diagram_type": "aws",
  "nodes": [
    {{"name": "LoadBalancer", "node_type": "ELB", "provider": "aws", "category": "network", "properties": {{"label": "Application Load Balancer"}}}},
    {{"name": "WebServer", "node_type": "EC2", "provider": "aws", "category": "compute", "properties": {{"label": "Web Server EC2"}}}}
  ],
  "connections": [
    {{"source": "LoadBalancer", "target": "WebServer", "label": "HTTP/HTTPS"}}
  ],
  "layout": "hierarchical",
  "metadata": {{"complexity": "medium", "estimated_cost": "low"}}
}}

Responde ÚNICAMENTE con el JSON válido, sin explicaciones adicionales."""

    async def generate_diagram_spec(self, request: DiagramRequest) -> DiagramSpec:
        """Genera una especificación de diagrama usando OpenAI"""
        try:
            system_prompt = self._create_system_prompt()
            
            # Crear el prompt del usuario con contexto adicional
            user_prompt = f"""Genera un diagrama para: {request.prompt}

Consideraciones adicionales:
- Título sugerido: {request.title or 'Generado automáticamente'}
- Tipo preferido: {request.diagram_type.value if request.diagram_type else 'automático'}
- Formato de salida: {request.output_format.value}

Por favor, crea una especificación completa y detallada."""

            # Llamada a OpenAI con structured outputs
            response = await self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format=DiagramSpecSchema,
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extraer y procesar la respuesta
            spec_data = response.choices[0].message.parsed
            
            # Convertir a entidades del dominio
            nodes = []
            for node_data in spec_data.nodes:
                nodes.append(DiagramNode(
                    name=node_data["name"],
                    node_type=node_data["node_type"],
                    provider=node_data["provider"],
                    category=node_data["category"],
                    properties=node_data.get("properties", {})
                ))
            
            connections = []
            for conn_data in spec_data.connections:
                connections.append(DiagramConnection(
                    source=conn_data["source"],
                    target=conn_data["target"],
                    label=conn_data.get("label"),
                    style=conn_data.get("style")
                ))
            
            # Mapear tipo de diagrama
            try:
                diagram_type = DiagramType(spec_data.diagram_type.lower())
            except ValueError:
                diagram_type = DiagramType.GENERIC
            
            return DiagramSpec(
                title=spec_data.title,
                description=spec_data.description,
                nodes=nodes,
                connections=connections,
                diagram_type=diagram_type,
                layout=spec_data.layout,
                metadata=spec_data.metadata
            )
            
        except Exception as e:
            raise AIProviderError(f"Error generating diagram spec: {str(e)}")
    
    async def validate_connection(self) -> bool:
        """Valida la conexión con OpenAI"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=1
            )
            return True
        except Exception:
            return False
    
    def get_provider_info(self) -> dict:
        """Obtiene información del proveedor OpenAI"""
        return {
            "name": "OpenAI",
            "model": self.model,
            "base_url": self.base_url or "https://api.openai.com/v1",
            "has_structured_outputs": True,
            "supports_async": True
        }