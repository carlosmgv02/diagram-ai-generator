from src.application.mcp.tools.base_tool import BaseTool, register_tool
from src.application.mcp.tools.tool_constants import LANGUAGE_INSTRUCTION

class ProvidersTool(BaseTool):
    @register_tool
    def list_providers(self) -> str:
        f"""
        List all available cloud providers and infrastructure platforms.
        
        {LANGUAGE_INSTRUCTION}
        
        This is STEP 1 of the recommended workflow for creating diagrams with correct icons.
        
        Returns:
            Numbered list of all available providers
        """
        providers_mapping = {
            "aws": "AWS - Amazon Web Services", 
            "azure": "Azure - Microsoft Azure",
            "gcp": "GCP - Google Cloud Platform",
            "k8s": "K8S - Kubernetes",
            "onprem": "OnPrem - On-premise services",
            "ibm": "IBM - IBM Cloud",
            "alibabacloud": "AlibabaCloud - Alibaba Cloud",
            "oci": "OCI - Oracle Cloud Infrastructure", 
            "openstack": "OpenStack",
            "firebase": "Firebase - Google Firebase",
            "digitalocean": "DigitalOcean",
            "elastic": "Elastic - Elastic Stack",
            "outscale": "Outscale Cloud",
            "generic": "Generic - Generic components",
            "programming": "Programming - Programming languages",
            "saas": "Saas - Software as a Service",
            "c4": "C4 - C4 Model diagrams",
            "custom": "Custom - Custom components"
        }
        
        response = "📋 AVAILABLE PROVIDERS\n\n"
        
        for i, (key, description) in enumerate(providers_mapping.items(), 1):
            response += f"{i}. **{key}** - {description}\n"
        
        response += f"\n✅ Total: {len(providers_mapping)} providers"
        response += f"\n\n➡️  NEXT STEP: get_provider_categories(\"provider_name\")"
        response += f"\n💡 Example: get_provider_categories(\"aws\") to see AWS categories"
        
        return response
