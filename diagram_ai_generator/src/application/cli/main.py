"""
Interfaz de línea de comandos principal
"""
import asyncio
import os
from pathlib import Path
from typing import Optional

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from ...domain.entities.diagram import DiagramRequest, DiagramType, OutputFormat
from ...domain.use_cases.generate_diagram_use_case import GenerateDiagramUseCase
from ...domain.use_cases.list_providers_use_case import ListProvidersUseCase
from ...infrastructure.adapters.openai_provider import OpenAIProvider
from ...infrastructure.adapters.diagrams_repository import DiagramsRepository

# Cargar variables de entorno
load_dotenv()

console = Console()


def create_dependencies():
    """Crea las dependencias para la aplicación"""
    ai_provider = OpenAIProvider()
    diagram_repository = DiagramsRepository()
    
    generate_use_case = GenerateDiagramUseCase(ai_provider, diagram_repository)
    list_providers_use_case = ListProvidersUseCase(diagram_repository)
    
    return generate_use_case, list_providers_use_case


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    🎨 Diagram AI Generator - Genera diagramas de arquitectura usando IA
    
    Una herramienta CLI para crear diagramas técnicos a partir de prompts en lenguaje natural.
    """
    pass


@cli.command()
@click.argument('prompt', required=True)
@click.option('--type', '-t', 'diagram_type', 
              type=click.Choice(['aws', 'azure', 'gcp', 'k8s', 'onprem', 'generic', 'programming', 'c4', 'custom']),
              help='Tipo de diagrama a generar')
@click.option('--format', '-f', 'output_format',
              type=click.Choice(['png', 'svg', 'pdf', 'dot']),
              default='png',
              help='Formato de salida del diagrama')
@click.option('--output', '-o', 'output_path',
              help='Ruta de salida del archivo')
@click.option('--title', '-T',
              help='Título personalizado para el diagrama')
def generate(prompt: str, diagram_type: Optional[str], output_format: str, output_path: Optional[str], title: Optional[str]):
    """
    Genera un diagrama basado en un prompt de texto.
    
    PROMPT: Descripción de la arquitectura a diagramar
    
    Ejemplo:
        diagram-ai generate "arquitectura web con load balancer, EC2 y RDS en AWS"
    """
    asyncio.run(_generate_diagram(prompt, diagram_type, output_format, output_path, title))


async def _generate_diagram(prompt: str, diagram_type: Optional[str], output_format: str, output_path: Optional[str], title: Optional[str]):
    """Función interna para generar diagramas (async)"""
    try:
        generate_use_case, _ = create_dependencies()
        
        # Crear solicitud
        request = DiagramRequest(
            prompt=prompt,
            diagram_type=DiagramType(diagram_type) if diagram_type else None,
            output_format=OutputFormat(output_format),
            output_path=output_path,
            title=title
        )
        
        # Mostrar información de la solicitud
        console.print(Panel.fit(f"🚀 Generando diagrama: [bold]{prompt}[/bold]", title="Diagram AI Generator"))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generando diagrama con IA...", total=None)
            
            # Generar diagrama
            result = await generate_use_case.execute(request)
            
            progress.update(task, description="✅ Completado")
        
        if result.success:
            console.print(f"\n✅ [bold green]Diagrama generado exitosamente![/bold green]")
            console.print(f"📁 Archivo: [bold]{result.file_path}[/bold]")
            console.print(f"⏱️  Tiempo: [dim]{result.generation_time:.2f}s[/dim]")
            
            if result.spec:
                console.print(f"\n📋 [bold]Especificación:[/bold]")
                console.print(f"   Título: {result.spec.title}")
                console.print(f"   Nodos: {len(result.spec.nodes)}")
                console.print(f"   Conexiones: {len(result.spec.connections)}")
                console.print(f"   Tipo: {result.spec.diagram_type.value}")
        else:
            console.print(f"\n❌ [bold red]Error generando diagrama:[/bold red]")
            console.print(f"   {result.error_message}")
            if result.generation_time:
                console.print(f"⏱️  Tiempo: [dim]{result.generation_time:.2f}s[/dim]")
    
    except Exception as e:
        console.print(f"\n💥 [bold red]Error inesperado:[/bold red] {str(e)}")


@cli.command()
@click.option('--provider', '-p',
              help='Filtrar por proveedor específico')
@click.option('--detailed', '-d', is_flag=True,
              help='Mostrar información detallada')
def list_providers(provider: Optional[str], detailed: bool):
    """
    Lista los proveedores de diagramas disponibles.
    
    Muestra todos los proveedores soportados (AWS, Azure, GCP, etc.)
    junto con sus categorías y estadísticas.
    """
    try:
        _, list_providers_use_case = create_dependencies()
        
        if provider:
            # Mostrar información de un proveedor específico
            _show_provider_details(list_providers_use_case, provider)
        else:
            # Mostrar resumen de todos los proveedores
            _show_providers_summary(list_providers_use_case, detailed)
    
    except Exception as e:
        console.print(f"\n💥 [bold red]Error:[/bold red] {str(e)}")


def _show_providers_summary(list_providers_use_case, detailed: bool):
    """Muestra resumen de todos los proveedores"""
    summary = list_providers_use_case.get_provider_summary()
    
    console.print(Panel.fit(
        f"📊 Total: [bold]{summary['total_providers']}[/bold] proveedores, "
        f"[bold]{summary['total_nodes']}[/bold] nodos disponibles",
        title="Proveedores de Diagramas"
    ))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Proveedor", style="cyan")
    table.add_column("Nodos", justify="right", style="green")
    table.add_column("Categorías", justify="right", style="yellow")
    
    if detailed:
        table.add_column("Ejemplos de Categorías", style="dim")
    
    for provider_name, stats in summary['providers'].items():
        categories_preview = ", ".join(stats['categories'][:3])
        if len(stats['categories']) > 3:
            categories_preview += f" (+{len(stats['categories']) - 3} más)"
        
        row = [
            stats['display_name'],
            str(stats['total_nodes']),
            str(stats['categories_count'])
        ]
        
        if detailed:
            row.append(categories_preview)
        
        table.add_row(*row)
    
    console.print(table)


def _show_provider_details(list_providers_use_case, provider_name: str):
    """Muestra detalles de un proveedor específico"""
    categories = list_providers_use_case.get_provider_categories(provider_name)
    
    if not categories:
        console.print(f"❌ [bold red]Proveedor '{provider_name}' no encontrado[/bold red]")
        return
    
    console.print(Panel.fit(
        f"Detalles del proveedor [bold]{provider_name.upper()}[/bold]",
        title="Información del Proveedor"
    ))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Categoría", style="cyan")
    table.add_column("Nodos", justify="right", style="green")
    table.add_column("Ejemplos", style="dim")
    
    for category in categories:
        examples = ", ".join(category.nodes[:5])
        if len(category.nodes) > 5:
            examples += f" (+{len(category.nodes) - 5} más)"
        
        table.add_row(
            category.name,
            str(len(category.nodes)),
            examples
        )
    
    console.print(table)


@cli.command()
@click.argument('query')
@click.option('--provider', '-p',
              help='Filtrar por proveedor específico')
@click.option('--limit', '-l', default=10,
              help='Límite de resultados (default: 10)')
def search(query: str, provider: Optional[str], limit: int):
    """
    Busca nodos disponibles por nombre.
    
    QUERY: Término de búsqueda para encontrar nodos
    
    Ejemplo:
        diagram-ai search "ec2"
        diagram-ai search "database" --provider aws
    """
    try:
        _, list_providers_use_case = create_dependencies()
        
        results = list_providers_use_case.search_nodes(query, provider)
        results = results[:limit]  # Limitar resultados
        
        if not results:
            console.print(f"❌ [yellow]No se encontraron nodos para '{query}'[/yellow]")
            return
        
        console.print(Panel.fit(
            f"🔍 Encontrados [bold]{len(results)}[/bold] nodos para '[bold]{query}[/bold]'",
            title="Resultados de Búsqueda"
        ))
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Nodo", style="cyan")
        table.add_column("Proveedor", style="green")
        table.add_column("Categoría", style="yellow")
        
        for node in results:
            table.add_row(
                node.name,
                node.provider.upper(),
                node.category
            )
        
        console.print(table)
    
    except Exception as e:
        console.print(f"\n💥 [bold red]Error:[/bold red] {str(e)}")


@cli.command()
async def test_connection():
    """
    Prueba la conexión con el proveedor de IA (OpenAI).
    """
    try:
        console.print("🔌 Probando conexión con OpenAI...")
        
        ai_provider = OpenAIProvider()
        is_connected = await ai_provider.validate_connection()
        
        if is_connected:
            provider_info = ai_provider.get_provider_info()
            console.print("✅ [bold green]Conexión exitosa![/bold green]")
            console.print(f"   Modelo: {provider_info['model']}")
            console.print(f"   URL: {provider_info['base_url']}")
        else:
            console.print("❌ [bold red]Error de conexión[/bold red]")
            console.print("   Verifica tu API key de OpenAI")
    
    except Exception as e:
        console.print(f"💥 [bold red]Error:[/bold red] {str(e)}")


def main():
    """Punto de entrada principal"""
    cli()


if __name__ == "__main__":
    main()