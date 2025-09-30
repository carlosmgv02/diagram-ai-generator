#!/bin/bash
# Build and release script for Diagram AI Generator

set -e

echo "🏗️  Building Diagram AI Generator for release..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Install build dependencies
echo "📦 Installing build dependencies..."
pip install --upgrade build twine

# Build the package
echo "🔨 Building package..."
python -m build

# Verify the build
echo "✅ Verifying build..."
twine check dist/*

echo ""
echo "✅ Build completed successfully!"
echo ""
echo "📦 Package files:"
ls -la dist/

echo ""
echo "🚀 To publish to PyPI:"
echo "   twine upload dist/*"
echo ""
echo "🐳 To build Docker image:"
echo "   docker build -f docker/Dockerfile -t diagram-ai-generator:latest ."
echo ""
echo "🧪 To test the package locally:"
echo "   pip install dist/diagram_ai_generator-*.whl"
