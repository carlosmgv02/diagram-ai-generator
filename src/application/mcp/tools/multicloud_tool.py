from src.application.mcp.tools.base_tool import BaseTool, register_tool

class MulticloudTool(BaseTool):
    @register_tool
    def multicloud_helper(self) -> str:
        """
        🌐 HERRAMIENTA ESPECÍFICA PARA DIAGRAMAS MULTI-CLOUD
        
        Explica cómo crear diagramas que incluyen múltiples proveedores cloud.
        
        Returns:
            Guía completa para diagramas multi-cloud con ejemplos
        """
        return """🌐 **GUÍA COMPLETA PARA DIAGRAMAS MULTI-CLOUD**

## 🎯 **NUEVA FUNCIONALIDAD: ICONOS ESPECÍFICOS EN MULTI-CLOUD**

⚠️ **OPCIONES DISPONIBLES:**
- OPCIÓN A: Iconos genéricos consistentes
- OPCIÓN B: Iconos específicos de cada proveedor (RECOMENDADO)

## ✅ **OPCIÓN B - ICONOS ESPECÍFICOS (NUEVO):**

```json
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
```

## 🔑 **PUNTOS CLAVE:**
1. **Provider base:** "generic" 
2. **Component_provider:** Especifica el proveedor real de cada componente
3. **Type:** Usa el nombre exacto del servicio (Lambda, FunctionApps, Functions)
4. **Resultado:** Iconos específicos de AWS, Azure, GCP en un mismo diagrama

## ✅ **VENTAJAS:**
- ✅ Iconos de AWS Lambda reales
- ✅ Iconos de Azure Functions reales  
- ✅ Iconos de GCP Functions reales
- ✅ Diagrama profesional multi-cloud

## 📋 **FLUJO RECOMENDADO:**
1. step2_get_categories("aws") → Ver categorías AWS
2. step3_get_nodes("aws", "compute") → Ver "Lambda"
3. step2_get_categories("azure") → Ver categorías Azure  
4. step3_get_nodes("azure", "compute") → Ver "FunctionApps"
5. step2_get_categories("gcp") → Ver categorías GCP
6. step3_get_nodes("gcp", "compute") → Ver "Functions"
7. Crear JSON con component_provider específico"""