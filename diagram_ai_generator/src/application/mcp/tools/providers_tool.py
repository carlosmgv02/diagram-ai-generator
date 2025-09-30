from src.application.mcp.tools.base_tool import BaseTool, register_tool

class ProvidersTool(BaseTool):
    @register_tool
    def step1_list_providers(self) -> str:
        """
        🔥 PASO 1 OBLIGATORIO: Lista todos los proveedores disponibles automáticamente.
        
        DEBES USAR ESTE PASO PRIMERO antes de cualquier diagrama.
        
        Returns:
            Lista numerada de todos los proveedores disponibles
        """
        providers_mapping = {
            "onprem": "OnPrem - Servicios on-premise",
            "aws": "AWS - Amazon Web Services", 
            "azure": "Azure - Microsoft Azure",
            "gcp": "GCP - Google Cloud Platform",
            "ibm": "IBM - IBM Cloud",
            "k8s": "K8S - Kubernetes",
            "alibabacloud": "AlibabaCloud - Alibaba Cloud",
            "oci": "OCI - Oracle Cloud Infrastructure", 
            "openstack": "OpenStack - OpenStack",
            "firebase": "Firebase - Google Firebase",
            "digitalocean": "DigitalOcean - DigitalOcean",
            "elastic": "Elastic - Elastic Stack",
            "outscale": "Outscale - Outscale Cloud",
            "generic": "Generic - Componentes genéricos",
            "programming": "Programming - Lenguajes de programación",
            "saas": "Saas - Software as a Service",
            "c4": "C4 - Diagramas C4",
            "custom": "Custom - Componentes personalizados",
            "gis": "GIS - Sistemas de información geográfica"
        }
        
        response = "🔥 **PASO 1: PROVEEDORES DISPONIBLES**\n\n"
        
        for i, (key, description) in enumerate(providers_mapping.items(), 1):
            response += f"{i}. **{key}** - {description}\n"
        
        response += f"\n✅ **Total:** {len(providers_mapping)} proveedores"
        response += f"\n\n🔥 **SIGUIENTE PASO OBLIGATORIO:** step2_get_categories(\"nombre_proveedor\")"
        response += f"\n💡 **Ejemplo:** step2_get_categories(\"aws\") para ver categorías de AWS"
        
        return response