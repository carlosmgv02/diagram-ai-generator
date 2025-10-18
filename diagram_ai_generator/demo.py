#!/usr/bin/env python3
"""
Demo script para Diagram AI Generator
Muestra las capacidades principales de la aplicación
"""
import asyncio
import os
import sys
from pathlib import Path

# Añadir el directorio src al path para importar los módulos
sys.path.insert(0, str(Path(__file__).parent / "src"))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.domain.entities.diagram import DiagramRequest, DiagramType, OutputFormat
from src.domain.use_cases.generate_diagram_use_case import GenerateDiagramUseCase
from src.domain.use_cases.list_providers_use_case import ListProvidersUseCase
from src.infrastructure.adapters.openai_provider import OpenAIProvider
from src.infrastructure.adapters.diagrams_repository import DiagramsRepository

console = Console()


def show_welcome():
    """Muestra mensaje de bienvenida"""
    console.print(Panel.fit(
        "🎨 [bold]Diagram AI Generator - Demo[/bold]\n"
        "Generador de diagramas de arquitectura usando IA",
        style="cyan"
    ))


def show_providers_info(list_providers_use_case):
    """Muestra información de proveedores disponibles"""
    console.print("\n📊 [bold]Proveedores Disponibles:[/bold]")
    
    summary = list_providers_use_case.get_provider_summary()
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Proveedor", style="cyan")
    table.add_column("Nodos", justify="right", style="green")
    table.add_column("Categorías", justify="right", style="yellow")
    table.add_column("Ejemplos", style="dim")
    
    for provider_name, stats in list(summary['providers'].items())[:5]:  # Top 5
        categories_preview = ", ".join(stats['categories'][:3])
        if len(stats['categories']) > 3:
            categories_preview += f" (+{len(stats['categories']) - 3})"
        
        table.add_row(
            stats['display_name'],
            str(stats['total_nodes']),
            str(stats['categories_count']),
            categories_preview
        )
    
    console.print(table)
    console.print(f"[dim]Total: {summary['total_providers']} proveedores, {summary['total_nodes']} nodos[/dim]")


async def demo_diagram_generation(generate_use_case):
    """Demuestra la generación de diagramas"""
    console.print("\n🚀 [bold]Demo: Generación de Diagrama[/bold]")
    
    # Ejemplo de arquitectura web
    prompt = "aplicación web escalable con load balancer, servidores web en múltiples zonas, base de datos con réplica de lectura, caché Redis y CDN"
    
    console.print(f"[dim]Prompt:[/dim] {prompt}")
    
    request = DiagramRequest(
        prompt=prompt,
        diagram_type=DiagramType.AWS,
        output_format=OutputFormat.PNG,
        title="Demo Web Architecture"
    )
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Generando diagrama con IA...", total=None)
        
        try:
            result = await generate_use_case.execute(request)
            progress.update(task, description="✅ Completado")
            
            if result.success:
                console.print(f"✅ [green]Diagrama generado exitosamente![/green]")
                console.print(f"📁 Archivo: [bold]{result.file_path}[/bold]")
                console.print(f"⏱️  Tiempo: [dim]{result.generation_time:.2f}s[/dim]")
                
                if result.spec:
                    console.print(f"\n📋 [bold]Especificación generada:[/bold]")
                    console.print(f"   Título: {result.spec.title}")
                    console.print(f"   Descripción: {result.spec.description}")
                    console.print(f"   Nodos: {len(result.spec.nodes)}")
                    console.print(f"   Conexiones: {len(result.spec.connections)}")
                    
                    # Mostrar algunos nodos
                    if result.spec.nodes:
                        console.print(f"\n   [bold]Nodos incluidos:[/bold]")
                        for node in result.spec.nodes[:5]:  # Primeros 5
                            console.print(f"   • {node.name} ({node.node_type})")
                        if len(result.spec.nodes) > 5:
                            console.print(f"   • ... y {len(result.spec.nodes) - 5} más")
            else:
                console.print(f"❌ [red]Error:[/red] {result.error_message}")
                
        except Exception as e:
            progress.update(task, description="❌ Error")
            console.print(f"💥 [red]Error inesperado:[/red] {str(e)}")


def demo_search_functionality(list_providers_use_case):
    """Demuestra la funcionalidad de búsqueda"""
    console.print("\n🔍 [bold]Demo: Búsqueda de Componentes[/bold]")
    
    # Buscar componentes de base de datos
    search_term = "database"
    console.print(f"[dim]Buscando:[/dim] {search_term}")
    
    results = list_providers_use_case.search_nodes(search_term, limit=8)
    
    if results:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Componente", style="cyan")
        table.add_column("Proveedor", style="green")
        table.add_column("Categoría", style="yellow")
        
        for node in results:
            table.add_row(node.name, node.provider.upper(), node.category)
        
        console.print(table)
        console.print(f"[dim]Mostrando {len(results)} de muchos resultados disponibles[/dim]")
    else:
        console.print("❌ No se encontraron resultados")


async def test_openai_connection():
    """Prueba la conexión con OpenAI"""
    console.print("\n🔌 [bold]Probando Conexión con OpenAI[/bold]")
    
    try:
        provider = OpenAIProvider()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Verificando conexión...", total=None)
            
            is_connected = await provider.validate_connection()
            
            if is_connected:
                progress.update(task, description="✅ Conectado")
                provider_info = provider.get_provider_info()
                console.print(f"✅ [green]Conexión exitosa con OpenAI[/green]")
                console.print(f"   Modelo: {provider_info['model']}")
                console.print(f"   URL: {provider_info['base_url']}")
                return True
            else:
                progress.update(task, description="❌ Error de conexión")
                console.print("❌ [red]No se pudo conectar con OpenAI[/red]")
                console.print("   Verifica tu API key en el archivo .env")
                return False
                
    except Exception as e:
        console.print(f"💥 [red]Error:[/red] {str(e)}")
        return False


def show_next_steps():
    """Muestra los próximos pasos"""
    console.print("\n🎯 [bold]Próximos Pasos:[/bold]")
    console.print("1. 🔑 Configura tu API key de OpenAI en el archivo .env")
    console.print("2. 🚀 Usa el CLI: [cyan]diagram-ai generate \"tu arquitectura aquí\"[/cyan]")
    console.print("3. 🔍 Explora proveedores: [cyan]diagram-ai list-providers[/cyan]")
    console.print("4. 🛠️  Ejecuta el servidor MCP para integración avanzada")
    console.print("5. 📚 Lee la documentación completa en README.md")


async def main():
    """Función principal del demo"""
    show_welcome()
    
    # Verificar configuración
    if not os.getenv("OPENAI_API_KEY"):
        console.print("\n⚠️  [yellow]API key de OpenAI no configurada[/yellow]")
        console.print("Para el demo completo, configura OPENAI_API_KEY en .env")
        console.print("Continuando con demo limitado...\n")
        demo_with_ai = False
    else:
        demo_with_ai = True
    
    try:
        # Crear dependencias
        diagram_repository = DiagramsRepository()
        list_providers_use_case = ListProvidersUseCase(diagram_repository)
        
        # Demo de proveedores (no requiere API key)
        show_providers_info(list_providers_use_case)
        demo_search_functionality(list_providers_use_case)
        
        if demo_with_ai:
            # Prueba de conexión
            ai_provider = OpenAIProvider()
            connection_ok = await test_openai_connection()
            
            if connection_ok:
                # Demo de generación
                generate_use_case = GenerateDiagramUseCase(ai_provider, diagram_repository)
                await demo_diagram_generation(generate_use_case)
            else:
                console.print("\n⚠️  [yellow]Saltando demo de generación debido a problemas de conexión[/yellow]")
        
        show_next_steps()
        
        console.print(Panel.fit(
            "🎉 [bold green]Demo completado![/bold green]\n"
            "Diagram AI Generator está listo para usar",
            style="green"
        ))
        
    except Exception as e:
        console.print(f"\n💥 [bold red]Error en el demo:[/bold red] {str(e)}")
        console.print("Verifica la instalación y configuración")


if __name__ == "__main__":
    asyncio.run(main())