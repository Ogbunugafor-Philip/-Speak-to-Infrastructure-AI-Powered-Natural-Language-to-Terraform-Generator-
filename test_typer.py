# test_typer.py
import typer
from typing import Optional
from enum import Enum
import sys

# Define choices as Enum for better type safety
class CloudProvider(str, Enum):
    AWS = "AWS"
    AZURE = "Azure"
    GCP = "GCP"

# Create a Typer app instance with enhanced configuration
app = typer.Typer(
    name="test-typer",
    help="🧪 A comprehensive test for our Typer CLI framework.",
    add_completion=False,
    no_args_is_help=True,
)

@app.command()
def hello(
    name: str = typer.Argument(..., help="Your name"),
    greeting: Optional[str] = typer.Option(
        "Hello",
        "--greeting",
        "-g",
        help="Custom greeting message"
    ),
    excited: bool = typer.Option(
        False,
        "--excited",
        "-e",
        help="Add excitement with exclamation marks"
    )
):
    """
    Say hello to someone with customizable options.
    
    Examples:
    
        python test_typer.py hello John
        
        python test_typer.py hello Jane --greeting "Good morning"
        
        python test_typer.py hello Bob --excited
    """
    punctuation = "!" if excited else "."
    message = f"{greeting} {typer.style(name, fg=typer.colors.GREEN, bold=True)}{punctuation} 👋"
    
    typer.echo(message)
    
    if excited:
        typer.echo(typer.style("🎉 So much energy!", fg=typer.colors.YELLOW))

@app.command()
def menu():
    """
    Test a menu-like selection, similar to what we'll build for the orchestrator.
    
    This demonstrates:
    - Confirmations
    - Prompts with choices (using Enum)
    - Conditional logic
    - Colored output
    """
    try:
        typer.echo("\n" + "="*50)
        typer.echo(typer.style("🧪 TYPER MENU TEST", fg=typer.colors.CYAN, bold=True))
        typer.echo("="*50 + "\n")
        
        if not typer.confirm("Do you want to proceed with the test?", default=True):
            typer.echo(typer.style("👋 Okay, maybe next time!", fg=typer.colors.YELLOW))
            raise typer.Exit(0)
        
        typer.echo(typer.style("\n✅ Great! Let's continue...\n", fg=typer.colors.GREEN))
        
        # Display options manually for better UX
        typer.echo("Available cloud providers:")
        typer.echo("  1. AWS")
        typer.echo("  2. Azure")
        typer.echo("  3. GCP")
        
        # Get user choice
        while True:
            choice = typer.prompt(
                "\nPlease enter the number (1-3) or provider name",
                default="1"
            ).strip()
            
            # Map input to provider
            choice_map = {
                "1": "AWS",
                "2": "Azure", 
                "3": "GCP",
                "aws": "AWS",
                "azure": "Azure",
                "gcp": "GCP"
            }
            
            cloud_provider = choice_map.get(choice.lower())
            
            if cloud_provider:
                break
            else:
                typer.echo(typer.style(
                    "❌ Invalid choice. Please enter 1, 2, 3, or a provider name.",
                    fg=typer.colors.RED
                ))
        
        typer.echo(f"\n✅ You selected: {typer.style(cloud_provider, fg=typer.colors.BLUE, bold=True)}")
        
        # Additional test: numeric input
        num_instances = typer.prompt(
            "\nHow many instances do you want to deploy?",
            type=int,
            default=1
        )
        
        if num_instances > 10:
            typer.echo(typer.style(
                f"⚠️  Warning: Deploying {num_instances} instances may be expensive!",
                fg=typer.colors.RED
            ))
            if not typer.confirm("Are you sure?", default=False):
                typer.echo("Deployment cancelled.")
                raise typer.Exit(0)
        
        # Success summary
        typer.echo("\n" + "="*50)
        typer.echo(typer.style("📋 SUMMARY", fg=typer.colors.CYAN, bold=True))
        typer.echo("="*50)
        typer.echo(f"Provider: {typer.style(cloud_provider, fg=typer.colors.BLUE)}")
        typer.echo(f"Instances: {typer.style(str(num_instances), fg=typer.colors.GREEN)}")
        typer.echo("="*50 + "\n")
        
        typer.echo(typer.style("✅ Menu test completed successfully!", fg=typer.colors.GREEN, bold=True))
        
    except typer.Abort:
        typer.echo("\n\n⚠️  Test aborted by user.")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(typer.style(f"\n❌ Error: {e}", fg=typer.colors.RED))
        raise typer.Exit(1)

@app.command()
def colors():
    """
    Display all available Typer colors for reference.
    """
    typer.echo("\n" + "="*50)
    typer.echo(typer.style("🎨 TYPER COLOR PALETTE", fg=typer.colors.MAGENTA, bold=True))
    typer.echo("="*50 + "\n")
    
    color_list = [
        ("BLACK", typer.colors.BLACK),
        ("RED", typer.colors.RED),
        ("GREEN", typer.colors.GREEN),
        ("YELLOW", typer.colors.YELLOW),
        ("BLUE", typer.colors.BLUE),
        ("MAGENTA", typer.colors.MAGENTA),
        ("CYAN", typer.colors.CYAN),
        ("WHITE", typer.colors.WHITE),
        ("BRIGHT_BLACK", typer.colors.BRIGHT_BLACK),
        ("BRIGHT_RED", typer.colors.BRIGHT_RED),
        ("BRIGHT_GREEN", typer.colors.BRIGHT_GREEN),
        ("BRIGHT_YELLOW", typer.colors.BRIGHT_YELLOW),
        ("BRIGHT_BLUE", typer.colors.BRIGHT_BLUE),
        ("BRIGHT_MAGENTA", typer.colors.BRIGHT_MAGENTA),
        ("BRIGHT_CYAN", typer.colors.BRIGHT_CYAN),
        ("BRIGHT_WHITE", typer.colors.BRIGHT_WHITE),
    ]
    
    for color_name, color_value in color_list:
        colored_text = typer.style(f"  ● {color_name}", fg=color_value, bold=True)
        typer.echo(colored_text)
    
    typer.echo("\n" + "="*50 + "\n")

@app.command()
def test_all():
    """
    Run all tests sequentially to verify Typer functionality.
    """
    typer.echo("\n" + "="*50)
    typer.echo(typer.style("🚀 RUNNING ALL TESTS", fg=typer.colors.CYAN, bold=True))
    typer.echo("="*50 + "\n")
    
    # Test 1: Hello command
    typer.echo(typer.style("Test 1: Hello Command", fg=typer.colors.YELLOW))
    typer.echo("  Testing with name='Tester'...")
    hello.callback(name="Tester", greeting="Hello", excited=False)
    typer.echo(typer.style("  ✅ Passed\n", fg=typer.colors.GREEN))
    
    # Test 2: Colors
    typer.echo(typer.style("Test 2: Color Display", fg=typer.colors.YELLOW))
    typer.echo("  ✅ Passed (colors shown below)\n")
    colors.callback()
    
    typer.echo(typer.style("\n✅ All automated tests passed!", fg=typer.colors.GREEN, bold=True))
    typer.echo("💡 Run 'python test_typer.py menu' for interactive menu test.\n")

if __name__ == "__main__":
    try:
        app()
    except KeyboardInterrupt:
        typer.echo("\n\n⚠️  Interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        typer.echo(typer.style(f"\n❌ Unexpected error: {e}", fg=typer.colors.RED))
        sys.exit(1)