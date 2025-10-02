# 🎬 SCRIPT COMPLETO - VIDEO YOUTUBE: DIAGRAM AI GENERATOR

**Canal:** Carlos Martínez
**Duración estimada:** 12-15 minutos
**Título sugerido:** "Cansado de hacer Diagramas? Creé mi propio Generador con IA | Python + MCP + Claude"

---

## 🎯 INTRODUCCIÓN (0:00 - 2:00)

**[PANTALLA: Logo/Intro del canal]**

"¡Hola! Soy Carlos Martínez y tengo que confesarte algo... **Siempre se me ha dado fatal hacer diagramas y me daba muchísima pereza**. Y no sé si te pasa lo mismo, pero cuando tengo que presentar un proyecto a un cliente o hacer un video explicando una arquitectura, siempre llega ese momento horrible de 'ay no... tengo que hacer el diagrama'."

**[MOSTRAR: Ejemplos de diagramas mal hechos o genéricos]**

"Me he visto mil veces en situaciones donde necesitaba enseñar la arquitectura de un proyecto, ya sea para explicársela a un cliente, para documentación, o para videos como este, y siempre acababa perdiendo horas arrastrando iconos, buscando los iconos correctos de AWS, tratando de que quede alineado..."

**[MOSTRAR: Ejemplos de diagramas generados automáticamente]**

"Así que pensé: 'Ya está, voy a desarrollar algo que me solucione este problema de una vez por todas'. Y como además llevaba un par de meses usando Claude - que me gusta mucho más que ChatGPT, la verdad - y no había desarrollado ningún MCP todavía, decidí hacer mi primer proyecto MCP."

**[MOSTRAR: Estructura del video en pantalla]**

"En este video te voy a enseñar el resultado: un generador de diagramas que me ha cambiado la vida, y que espero que también te ayude a ti. Vamos a ver:
- Por qué este proyecto me resolvió un problema real
- Cómo funciona la magia por detrás
- Instalación y uso práctico
- Integración total con Claude Desktop
- Y por supuesto, código completo en GitHub"

---

## 🤔 EL PROBLEMA QUE ME LLEVÓ A ESTO (2:00 - 3:30)

**[MOSTRAR: Screenshots de herramientas como Lucidchart, Draw.io]**

"A ver, no es que no hubiera herramientas para hacer diagramas. Están Draw.io, Lucidchart, Visio... pero todas tienen el mismo problema para mí:"

**[MOSTRAR: Proceso manual tedioso]**

"❌ **Trabajo manual**: Tienes que arrastrar cada iconito uno por uno
❌ **Iconos genéricos**: O usas iconos feos y genéricos, o te pasas una hora buscando el icono exacto de 'AWS Lambda' vs 'AWS API Gateway'
❌ **Inconsistencias**: Un día usas un estilo de AWS, otro día otro, y al final tienes diagramas que parecen de proyectos diferentes
❌ **No escalable**: Si quieres cambiar algo, a reorganizar todo manualmente"

**[MOSTRAR: Claude en acción]**

"Y como ya llevaba un par de meses usando Claude para casi todo mi desarrollo - sinceramente me gusta más que ChatGPT para programar - se me ocurrió: '¿Y si pudiera simplemente decirle a Claude "hazme un diagrama de esta arquitectura" y que él me lo genere automáticamente?'"

**[MOSTRAR: MCP Protocol]**

"Ahí descubrí el MCP (Model Context Protocol) que permite extender Claude con herramientas personalizadas. Era la excusa perfecta para hacer mi primer proyecto MCP y solucionar mi problema con los diagramas de una tacada."

---

## 💡 LA SOLUCIÓN: DIAGRAM AI GENERATOR (3:30 - 5:00)

**[MOSTRAR: README.md del proyecto]**

"Y así nació Diagram AI Generator. El concepto es súper simple pero poderoso:"

**[MOSTRAR: Ejemplo de JSON → Diagrama]**

"Tú describes tu arquitectura en JSON - que es mucho más rápido que arrastrar iconos - y el sistema te genera un diagrama profesional con los iconos oficiales de cada proveedor."

**[MOSTRAR: Características principales]**

"Lo que lo hace especial para mí:

✅ **Iconos reales**: Usa los iconos oficiales de AWS, Azure, GCP... nada de iconos genéricos feos
✅ **Multi-cloud**: Puedo mezclar servicios de diferentes proveedores en un solo diagrama
✅ **Integración con Claude**: Le digo a Claude lo que quiero y él me genera el JSON automáticamente
✅ **Sugerencias inteligentes**: Si escribo 'DynamoDB' mal, automáticamente me sugiere 'Dynamodb'
✅ **Escalable**: Cambiar algo es modificar una línea en JSON, no reorganizar todo el diagrama"

**[MOSTRAR: Comparación antes/después]**

"Antes: 2 horas haciendo un diagrama manualmente
Ahora: 5 minutos escribiendo el JSON o simplemente diciéndole a Claude lo que quiero"

**[MOSTRAR: Casos de uso reales]**

"Y esto me ha resuelto problemas reales:
- Presentaciones a clientes: diagramas profesionales en minutos
- Videos como este: la arquitectura se explica sola
- Documentación de proyectos: siempre consistente y actualizable"

---

## 🏗️ CÓMO FUNCIONA POR DETRÁS (5:00 - 6:30)

**[MOSTRAR: Estructura de directorios]**

"Vamos a ver rápidamente cómo está estructurado porque seguí buenas prácticas de arquitectura:"

```
src/
├── application/           # La lógica de aplicación
│   ├── mcp/              # Servidor MCP y herramientas
│   │   ├── server_modular.py
│   │   └── tools/        # 5 herramientas para Claude
│   └── services/         # El motor principal
│       └── diagram_service.py
└── infrastructure/       # Datos de proveedores
    └── external/
        └── diagrams_structure.json  # 14+ proveedores
```

**[MOSTRAR: DiagramService código brevemente]**

"El corazón es el `DiagramService` que:
- Carga automáticamente todos los servicios de AWS, Azure, GCP...
- Hace importación dinámica para usar los iconos correctos
- Implementa las sugerencias inteligentes que me han salvado mil veces
- Optimiza las imágenes para que no pesen una barbaridad"

**[MOSTRAR: MCP Tools]**

"Y las 5 herramientas MCP que permiten que Claude funcione como mi asistente personal de diagramas:
1. `step1_list_providers` - '¿Qué proveedores hay?'
2. `step2_get_categories` - '¿Qué categorías tiene AWS?'
3. `step3_get_nodes` - '¿Cómo se llama exactamente Lambda en el código?'
4. `create_diagram_from_json` - 'Genera el diagrama'
5. `multicloud_helper` - 'Ayúdame con un diagrama multi-cloud'"

**[MOSTRAR: Python diagrams library]**

"Todo esto está construido sobre la librería `diagrams` de Python, que es genial porque ya tiene todos los iconos oficiales de todos los proveedores. Yo simplemente hice la capa de abstracción para usarla de forma inteligente."

---

## 💻 INSTALACIÓN RÁPIDA (6:30 - 7:30)

**[MOSTRAR: Terminal - proceso completo]**

"La instalación es súper directa. Te muestro las tres opciones, pero yo uso la de desarrollo:"

```bash
# Opción 1: Desde PyPI (la más fácil)
pip install diagram-ai-generator
diagram-ai-mcp

# Opción 2: Desarrollo (mi favorita)
git clone https://github.com/tu-usuario/diagram-ai-generator.git
cd diagram-ai-generator
pip install -e .

# Opción 3: Docker (para producción)
./scripts/run_docker.sh
```

**[MOSTRAR: Verificar que funciona]**

```bash
# Verificar instalación
python3 -c "from src import DiagramService; print('✅ Listo para crear diagramas!')"
```

**[MOSTRAR: Dependencias]**

"Las dependencias son mínimas - solo diagrams, Pillow y MCP. Ah, y necesitas Graphviz instalado:"

```bash
# Mac
brew install graphviz

# Ubuntu/Debian
sudo apt-get install graphviz
```

"Los diagramas se guardan automáticamente en `generated_diagrams/` - nunca más voy a perder un diagrama."

---

## 🔧 DEMO 1: MI PRIMER DIAGRAMA (7:30 - 9:00)

**[MOSTRAR: Editor con JSON]**

"Vamos con la demo real. Te voy a mostrar cómo creo un diagrama de una arquitectura serverless típica - algo que antes me llevaba una hora y ahora hago en 2 minutos:"

```json
{
  "title": "Mi Arquitectura Serverless",
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
      "label": "Función Lambda"
    },
    {
      "id": "dynamodb",
      "type": "Dynamodb",
      "category": "database",
      "label": "Base de Datos"
    }
  ],
  "connections": [
    {
      "from": "api_gateway",
      "to": "lambda",
      "color": "darkgreen",
      "style": "bold",
      "label": "HTTP Request"
    },
    {
      "from": "lambda",
      "to": "dynamodb",
      "color": "blue",
      "label": "Query/Write"
    }
  ]
}
```

**[MOSTRAR: Ejecutar el código]**

```python
from src.application.services.diagram_service import DiagramService

service = DiagramService()
result = service.create_diagram_from_spec(mi_arquitectura)
print(f"✅ Diagrama creado: {result['file_path']}")
```

**[MOSTRAR: Diagrama resultante]**

"¡Boom! Y aquí tienes el diagrama que antes me hubiera llevado una hora. Fíjate:
- Iconos oficiales de AWS, no genéricos
- Conexiones etiquetadas y con estilos
- Layout horizontal como especifiqué
- Listo para presentar a cualquier cliente"

---

## 🌐 DEMO 2: LO QUE MÁS ME GUSTA - MULTI-CLOUD (9:00 - 10:30)

**[MOSTRAR: JSON multi-cloud]**

"Pero lo que realmente me voló la cabeza fue poder hacer diagramas multi-cloud. Esto antes era imposible sin verse como un Frankenstein:"

```json
{
  "title": "Arquitectura Multi-Cloud Real",
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
      "id": "gcp_storage",
      "type": "Storage",
      "category": "storage",
      "component_provider": "gcp",
      "label": "Google Storage"
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
      "name": "Google Cloud",
      "components": ["gcp_storage"]
    }
  ]
}
```

**[MOSTRAR: Resultado del diagrama]**

"Mira esto - cada servicio mantiene su icono oficial, pero todo en un diagrama coherente. Esto es oro puro para:
- Explicar arquitecturas híbridas a clientes
- Documentar migraciones entre clouds
- Mostrar estrategias multi-cloud"

**[MOSTRAR: Antes vs Ahora]**

"Antes: 'Mejor no hago el diagrama multi-cloud porque va a quedar fatal'
Ahora: 'En 5 minutos tengo el diagrama perfecto'"

---

## 🧠 LA MAGIA: SUGERENCIAS INTELIGENTES (10:30 - 11:30)

**[MOSTRAR: Ejemplo de error intencional]**

"Una de las cosas que más me gustan es que el sistema me corrige automáticamente. Mira qué pasa si escribo mal un servicio:"

```json
{
  "id": "db",
  "type": "DynamoDB",  // ❌ Mal escrito
  "category": "database"
}
```

**[MOSTRAR: Console output]**

```
⚠️  NODO NO ENCONTRADO: 'DynamoDB' en aws/database
💡 SUGERENCIAS: Dynamodb, DocumentdbMongodbCompatibility
✅ USANDO SUGERENCIA: 'Dynamodb' en lugar de 'DynamoDB'
```

"El sistema me salva automáticamente de errores típicos que cometía siempre:
- `DynamoDB` → `Dynamodb` (camelCase vs PascalCase)
- `EventBridge` → `Eventbridge`
- `S3` → `SimpleStorageServiceS3`
- `PubSub` → `Pubsub`"

**[MOSTRAR: Función de búsqueda]**

"Y si no sé cómo se llama algo exactamente:"

```python
# Buscar servicios que contengan 'database'
results = service.search_nodes("database", "aws")
for result in results[:5]:
    print(f"- {result['name']}")
```

"Esto me ha ahorrado literalmente horas de ir a buscar documentación o probar nombres."

---

## 🔗 LA INTEGRACIÓN CON CLAUDE QUE CAMBIÓ TODO (11:30 - 13:00)

**[MOSTRAR: Terminal ejecutando MCP server]**

"Pero la verdadera magia viene con la integración MCP. Una vez que ejecutas el servidor:"

```bash
python3 scripts/run_mcp_server.py
```

**[MOSTRAR: Claude Desktop configurado]**

"Y lo configuras en Claude Desktop, puedo hacer cosas como esta:"

**[SIMULAR conversación con Claude]**

**Yo:** "Claude, necesito un diagrama de una arquitectura para un e-commerce con AWS. Incluye frontend, API, base de datos y sistema de pagos."

**Claude:** "Te ayudo a crear ese diagrama. Primero voy a ver qué servicios de AWS tenemos disponibles..."

*[Usa step1_list_providers, step2_get_categories, step3_get_nodes]*

**Claude:** "Perfecto, he creado un diagrama con:
- CloudFront para el frontend
- API Gateway para la API
- Lambda para el procesamiento
- DynamoDB para la base de datos
- Cognito para autenticación
- Stripe connect para pagos"

*[Usa create_diagram_from_json]*

**[MOSTRAR: Diagrama resultante]**

"¡Y voilà! Claude me acaba de crear un diagrama profesional entendiendo mi petición en lenguaje natural. Esto es lo que me ha cambiado completamente el workflow."

**[MOSTRAR: Otros ejemplos de comandos]**

"Otros comandos que uso constantemente:
- 'Hazme un diagrama de microservicios en Kubernetes'
- 'Necesito documentar una migración de Azure a AWS'
- 'Crea un diagrama de CI/CD completo'
- 'Explícame esta arquitectura con un diagrama'"

---

## 🎯 IMPACTO REAL EN MI TRABAJO (13:00 - 14:00)

**[MOSTRAR: Ejemplos de proyectos reales]**

"Te voy a ser honesto sobre el impacto real que esto ha tenido en mi trabajo:"

**[MOSTRAR: Métricas de tiempo]**

"✅ **Tiempo de creación**: De 2-3 horas → 5-10 minutos
✅ **Calidad**: Diagramas consistentes y profesionales siempre
✅ **Productividad**: Puedo hacer diagramas para todos mis videos y proyectos
✅ **Clientes más contentos**: Documentación visual clara desde el primer día"

**[MOSTRAR: Casos de uso reales]**

"Casos reales donde me ha salvado la vida:
- **Presentaciones a clientes**: Ya no postergo hacer el diagrama
- **Videos de YouTube**: Cada arquitectura tiene su diagrama explicativo
- **Documentación de proyectos**: Todo proyecto tiene diagramas actualizados
- **Propuestas comerciales**: Diagramas que venden la solución visualmente"

**[MOSTRAR: Feedback de clientes]**

"Y lo mejor: los clientes lo notan. Me han comentado que se ve mucho más profesional tener toda la documentación visual clara desde el principio."

---

## 🔧 BONUS: DOCKER Y PRODUCCIÓN (14:00 - 14:30)

**[MOSTRAR: Docker setup]**

"Como bonus, si quieres usar esto en producción o compartirlo con tu equipo:"

```bash
# Docker Compose para desarrollo
cd docker
docker-compose up -d

# O build para producción
docker build -f docker/Dockerfile -t diagram-ai-generator .
docker run -d -p 8080:8080 -v $(pwd)/generated_diagrams:/app/generated_diagrams diagram-ai-generator
```

"Perfecto para integrarlo en pipelines de CI/CD o tenerlo como servicio interno en la empresa."

---

## 🎯 CONCLUSIÓN Y PRÓXIMOS PASOS (14:30 - 15:00)

**[MOSTRAR: GitHub repo]**

"Y eso es todo! Este proyecto me resolvió un problema real que tenía desde hace años, y espero que a ti también te ayude. Ya no hay excusa para no hacer diagramas profesionales."

**[MOSTRAR: Estadísticas del proyecto]**

"Lo que hemos construido:
✅ Soporte para 14+ proveedores cloud
✅ 400+ servicios de AWS, 300+ de Azure, 200+ de GCP
✅ Integración nativa con Claude mediante MCP
✅ Sugerencias inteligentes que te ahorran tiempo
✅ Docker ready para producción"

**[MOSTRAR: Call to action]**

"Si este proyecto te puede ahorrar tiempo como me lo ahorró a mí:
- 👍 Dale like para que YouTube sepa que este contenido ayuda
- 🔔 Suscríbete porque voy a seguir compartiendo proyectos que resuelven problemas reales
- ⭐ Dale una estrella al repo en GitHub
- 💬 Cuéntame en comentarios: ¿qué te da más pereza hacer cuando programas?"

**[MOSTRAR: Links y recursos]**

"**Todo el código y documentación:**
- 📁 GitHub: github.com/tu-usuario/diagram-ai-generator
- 📚 Documentación completa en el README
- 🐛 Si encuentras bugs, repórtalos en Issues
- 💡 Ideas y mejoras en GitHub Discussions"

**[MOSTRAR: Próximos videos]**

"Próximos videos que tengo planeados:
- Más proyectos MCP que resuelven problemas reales
- Automatización de documentación con IA
- Integración de Claude en workflows de desarrollo"

"¡Gracias por ver el video y nos vemos en el próximo! Y recuerda: si algo te da pereza, probablemente se pueda automatizar 😉"

---

## 📝 NOTAS PARA LA GRABACIÓN

### 🎬 Tono y estilo:
- **Personal y auténtico**: "Me pasaba esto, me frustaba aquello"
- **Problema → Solución**: Estructura clara
- **Ejemplos reales**: No demos artificiales
- **Honesto sobre beneficios**: Métricas reales de tiempo ahorrado

### 🎯 Puntos emocionales clave:
1. **Frustración inicial**: "Se me daba fatal y me daba pereza"
2. **Momento eureka**: "Claude + MCP = solución perfecta"
3. **Satisfacción**: "Me cambió el workflow completamente"
4. **Compartir valor**: "Espero que te ayude como me ayudó a mí"

### ⏱️ Estructura temporal:
- **Hook fuerte**: Problema personal relatable (2 min)
- **Solución y demos**: Core técnico (8 min)
- **Integración Claude**: Diferenciador clave (3 min)
- **Impacto real**: Value proof (2 min)

### 🎬 Preparación de pantalla:
- **Terminal**: Fuente grande, tema oscuro
- **Editor**: VS Code con tema claro/oscuro según preferencia
- **Browser**: Tabs listos con GitHub, docs, etc.
- **Ejemplos**: JSON preparados en archivos separados

### 🔧 Backup plans:
- Si falla MCP: Mostrar solo la parte de Python
- Si falla internet: Todo local preparado
- Screenshots de respaldo para cada demo

---

**¡Éxito con tu video Carlos! 🚀**