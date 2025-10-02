#!/bin/bash
# Script completo para publicar en PyPI

set -e

echo "📦 Preparando publicación en PyPI..."

# Verificar que estamos en el directorio correcto
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar Python
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "🐍 Python version: $python_version"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
    echo "✅ Python $python_version es compatible (>= 3.9)"
else
    echo "❌ Python 3.9+ es requerido. Versión actual: $python_version"
    exit 1
fi

# Limpiar builds anteriores
echo "🧹 Limpiando builds anteriores..."
rm -rf build/ dist/ *.egg-info/ src/*.egg-info/

# Instalar dependencias de build
echo "📦 Instalando dependencias de build..."
pip install --upgrade build twine

# Verificar que los archivos importantes existen
echo "🔍 Verificando archivos del proyecto..."
required_files=("README.md" "LICENSE" "pyproject.toml" "src/__init__.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Archivo faltante: $file"
        exit 1
    fi
    echo "✅ $file"
done

# Verificar estructura de datos
if [ ! -f "src/infrastructure/external/diagrams_structure.json" ]; then
    echo "❌ Archivo de datos faltante: diagrams_structure.json"
    exit 1
fi
echo "✅ diagrams_structure.json"

# Build del paquete
echo "🔨 Construyendo paquete..."
python -m build

# Verificar el build
echo "✅ Verificando build..."
twine check dist/*

echo ""
echo "📊 Archivos generados:"
ls -la dist/

echo ""
echo "🎉 ¡Build completado exitosamente!"
echo ""
echo "📋 Próximos pasos:"
echo ""
echo "1️⃣  **Test en PyPI Test (Recomendado primero):**"
echo "   twine upload --repository testpypi dist/*"
echo "   # Luego instala y prueba:"
echo "   pip install --index-url https://test.pypi.org/simple/ diagram-ai-generator"
echo ""
echo "2️⃣  **Publicar en PyPI Production:**"
echo "   twine upload dist/*"
echo ""
echo "3️⃣  **Verificar instalación:**"
echo "   pip install diagram-ai-generator"
echo "   diagram-ai-mcp"
echo ""
echo "🔑 **Necesitarás:**"
echo "   - Cuenta en PyPI: https://pypi.org/account/register/"
echo "   - Token de API: https://pypi.org/manage/account/token/"
echo "   - Configurar ~/.pypirc con tu token"
echo ""
echo "💡 **Comandos útiles:**"
echo "   - Ver info del paquete: twine check dist/*"
echo "   - Subir solo wheel: twine upload dist/*.whl"
echo "   - Subir solo tarball: twine upload dist/*.tar.gz"
