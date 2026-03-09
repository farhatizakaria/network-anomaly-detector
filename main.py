#!/usr/bin/env python3
"""
🌐 Network Anomaly Detector - Modern TUI/CLI Application
Detects network anomalies including loops, packet loss, and latency issues.
Requires root/admin privileges for packet capture.
"""

import sys
import os
from typing import Optional
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.syntax import Syntax
from rich.status import Status
import questionary
from questionary import Style

from anomaly_detector import AnomalyDetector
from anomaly_detector.platform_utils import PlatformInfo


# Initialize rich console for beautiful output
console = Console()
app = typer.Typer(
    help="🌐 Network Anomaly Detector - Detect network anomalies with style!",
    pretty_exceptions_show_locals=False
)

# Custom style for questionary
CUSTOM_STYLE = Style([
    ('qmark', 'fg:#FF6B6B bold'),
    ('question', 'fg:#4ECDC4 bold'),
    ('answer', 'fg:#95E1D3 bold'),
    ('pointer', 'fg:#FF6B6B bold'),
    ('highlighted', 'fg:#FF6B6B bold'),
    ('selected', 'fg:#95E1D3'),
    ('separator', 'fg:#6C757D'),
    ('instruction', 'fg:#6C757D italic'),
])


def print_header():
    """Print beautiful application header."""
    header_text = """
    ╔════════════════════════════════════════════════════════╗
    ║       🌐 NETWORK ANOMALY DETECTOR v2.0 🌐             ║
    ║    Detect Loops, Packet Loss & Latency Issues         ║
    ╚════════════════════════════════════════════════════════╝
    """
    console.print(Panel.fit(header_text, border_style="cyan", padding=(1, 2)))


def print_platform_info():
    """Print system and platform information."""
    system = PlatformInfo.get_system()
    is_admin = PlatformInfo.require_admin()
    
    status_table = Table(show_header=False, box=None, padding=(0, 2))
    status_table.add_row(
        "[cyan]System:[/cyan]",
        f"[yellow]{system}[/yellow]"
    )
    status_table.add_row(
        "[cyan]Privileges:[/cyan]",
        f"[green]✓ Admin/Root[/green]" if is_admin else "[red]✗ Standard User[/red]"
    )
    
    console.print(status_table)
    
    if not is_admin:
        console.print(
            Panel(
                "[bold red]⚠️  WARNING:[/bold red] Running without admin/root privileges\n"
                f"Packet capture may fail or be limited.\n"
                f"[dim]On Linux/macOS: Use 'sudo python main.py' or enable capabilities\n"
                f"On Windows: Right-click cmd/PowerShell and 'Run as administrator'[/dim]",
                style="red"
            )
        )


def format_results(results: dict) -> None:
    """Display results in a beautiful formatted way."""
    if not results:
        console.print("[red]✗ No results to display[/red]")
        return
    
    # Loops table
    if results.get('loops'):
        loops_table = Table(title="[bold cyan]🔄 Routing Loops Detected[/bold cyan]", show_header=True)
        loops_table.add_column("ID", style="cyan")
        loops_table.add_column("Path", style="magenta")
        loops_table.add_column("TTL Variance", style="yellow")
        
        for i, loop in enumerate(results['loops'], 1):
            loops_table.add_row(
                str(i),
                str(loop.get('path', 'Unknown')),
                f"{loop.get('ttl_variance', 'N/A'):.2f}"
            )
        console.print(loops_table)
        console.print()
    
    # Packet loss table
    if results.get('losses'):
        loss_table = Table(title="[bold yellow]📉 Packet Loss Events[/bold yellow]", show_header=True)
        loss_table.add_column("Event", style="cyan")
        loss_table.add_column("Loss %", style="red")
        loss_table.add_column("Packets Analyzed", style="green")
        
        for i, loss in enumerate(results['losses'], 1):
            loss_pct = loss.get('loss_percentage', 0)
            loss_style = "red" if loss_pct > 10 else "yellow" if loss_pct > 5 else "green"
            loss_table.add_row(
                f"Event {i}",
                f"[{loss_style}]{loss_pct:.2f}%[/{loss_style}]",
                str(loss.get('packets_analyzed', 'N/A'))
            )
        console.print(loss_table)
        console.print()
    
    # Latency table
    if results.get('latencies'):
        latency_table = Table(title="[bold magenta]⚡ Latency Anomalies[/bold magenta]", show_header=True)
        latency_table.add_column("Anomaly", style="cyan")
        latency_table.add_column("Value (ms)", style="red")
        latency_table.add_column("Severity", style="yellow")
        
        for i, latency in enumerate(results['latencies'], 1):
            lat_ms = latency.get('latency_ms', 0)
            severity = "CRITICAL" if lat_ms > 500 else "HIGH" if lat_ms > 200 else "MEDIUM"
            severity_style = "red" if severity == "CRITICAL" else "yellow" if severity == "HIGH" else "yellow"
            latency_table.add_row(
                f"Spike {i}",
                f"[red]{lat_ms:.2f}[/red]",
                f"[{severity_style}]{severity}[/{severity_style}]"
            )
        console.print(latency_table)
        console.print()
    
    # Summary
    console.print("[bold cyan]Summary:[/bold cyan]")
    summary = Table(show_header=False, box=None, padding=(0, 2))
    summary.add_row(f"[cyan]Loops:[/cyan]", f"[yellow]{len(results.get('loops', []))}[/yellow]")
    summary.add_row(f"[cyan]Loss Events:[/cyan]", f"[yellow]{len(results.get('losses', []))}[/yellow]")
    summary.add_row(f"[cyan]Latency Anomalies:[/cyan]", f"[yellow]{len(results.get('latencies', []))}[/yellow]")
    console.print(summary)


def run_analysis(
    interface: Optional[str] = None,
    timeout: int = 10,
    packets: int = 100,
    latency_threshold: int = 100,
    loss_threshold: float = 5.0
) -> int:
    """Execute network analysis with progress indication."""
    try:
        config = {
            'packet_count': packets,
            'latency_threshold_ms': latency_threshold,
            'loss_threshold': loss_threshold,
        }
        
        console.print()
        console.print("[bold cyan]─────────────────────────────────────────[/bold cyan]")
        console.print("[bold]Configuration:[/bold]")
        config_table = Table(show_header=False, box=None, padding=(0, 2))
        config_table.add_row("[cyan]Interface:[/cyan]", interface or "[dim]auto-detect[/dim]")
        config_table.add_row("[cyan]Timeout:[/cyan]", f"{timeout}s")
        config_table.add_row("[cyan]Packets:[/cyan]", str(packets))
        config_table.add_row("[cyan]Latency Threshold:[/cyan]", f"{latency_threshold}ms")
        config_table.add_row("[cyan]Loss Threshold:[/cyan]", f"{loss_threshold}%")
        console.print(config_table)
        console.print("[bold cyan]─────────────────────────────────────────[/bold cyan]")
        console.print()
        
        detector = AnomalyDetector(interface=interface, config=config)
        
        # Progress bar with spinner
        with Progress(
            SpinnerColumn(style="cyan"),
            TextColumn("[bold cyan]{task.description}[/bold cyan]"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console,
            transient=False,
        ) as progress:
            task = progress.add_task(
                f"[cyan]Analyzing network traffic...     [/cyan]",
                total=timeout
            )
            
            import time
            detector_task = detector.analyze(timeout=timeout)
            
            # Simulate progress for demo purposes
            for i in range(timeout):
                time.sleep(1)
                progress.update(task, advance=1)
            
            results = detector_task if isinstance(detector_task, dict) else None
        
        console.print()
        
        if results:
            # Summary panel
            has_anomalies = (
                bool(results.get('loops')) or 
                bool(results.get('losses')) or 
                bool(results.get('latencies'))
            )
            
            if has_anomalies:
                console.print(
                    Panel(
                        "[bold red]🚨 ANOMALIES DETECTED![/bold red]",
                        style="red",
                        border_style="red"
                    )
                )
            else:
                console.print(
                    Panel(
                        "[bold green]✓ Network Status: HEALTHY[/bold green]",
                        style="green",
                        border_style="green"
                    )
                )
            
            console.print()
            format_results(results)
            
            # Check if fallback was used
            if results.get('analysis_mode') == 'fallback':
                console.print()
                console.print(
                    Panel(
                        "[dim]ℹ️  Note: Using Pure Python Monitor[/dim]\n"
                        "[dim]For advanced packet analysis, try:[/dim]\n"
                        "[cyan]sudo python main.py[/cyan]",
                        style="dim"
                    )
                )
            
            return 0
        else:
            console.print("[red]✗ Analysis failed - no results[/red]")
            return 1
    
    except KeyboardInterrupt:
        console.print("\n[yellow]⏸  Analysis interrupted by user[/yellow]")
        return 130
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        return 1


@app.command()
def main(
    interface: Optional[str] = typer.Option(
        None,
        "--interface", "-i",
        help="Network interface to monitor (e.g., eth0, en0)"
    ),
    timeout: int = typer.Option(
        10,
        "--timeout", "-t",
        help="Capture timeout in seconds",
        min=1,
        max=300
    ),
    packets: int = typer.Option(
        100,
        "--packets", "-p",
        help="Number of packets to capture",
        min=10,
        max=10000
    ),
    latency_threshold: int = typer.Option(
        100,
        "--latency-threshold",
        help="Latency threshold in milliseconds",
        min=10,
        max=5000
    ),
    loss_threshold: float = typer.Option(
        5.0,
        "--loss-threshold",
        help="Packet loss threshold percentage",
        min=0.1,
        max=100
    ),
    interactive: bool = typer.Option(
        False,
        "--interactive",
        help="Launch interactive mode"
    ),
):
    """
    🌐 Network Anomaly Detector - Advanced network monitoring tool
    
    Detects:
    • 🔄 Routing loops (TTL variance analysis)
    • 📉 Packet loss (sequence inspection)
    • ⚡ Latency spikes (statistical analysis)
    
    Examples:
    
    \b
    # Interactive mode (recommended)
    python main.py --interactive
    
    # Monitor with defaults
    python main.py
    
    # Custom configuration
    python main.py -i eth0 -t 15 -p 200
    """
    
    print_header()
    print_platform_info()
    
    # Interactive mode
    if interactive or (len(sys.argv) == 1):
        console.print("[bold cyan]🚀 Welcome to Network Anomaly Detector![/bold cyan]\n")
        
        # Ask for mode
        mode = questionary.select(
            "What would you like to do?",
            choices=[
                "🚀 Quick Analysis (default settings)",
                "⚙️  Custom Analysis",
                "❓ Help & Information",
                "❌ Exit"
            ],
            style=CUSTOM_STYLE,
        ).ask()
        
        if not mode or "Exit" in mode:
            console.print("[yellow]👋 Goodbye![/yellow]")
            raise typer.Exit(0)
        
        if "Help" in mode:
            console.print(Syntax("""
# Network Anomaly Detector - Advanced Usage

## Detection Types

### 1. Routing Loops 🔄
Detects circular routing patterns by analyzing TTL (Time To Live) values.
Higher TTL variance indicates potential loops.

### 2. Packet Loss 📉
Monitors packet sequence numbers to identify missing packets.
Helps diagnose connection quality issues.

### 3. Latency Anomalies ⚡
Uses statistical analysis (Z-scores) to detect unusual latency spikes.
Identifies jitter and performance degradation.

## Tips for Best Results

• Run with elevated privileges (sudo on Linux/macOS)
• Monitor during periods of network activity
• Increase packet count for more accurate results
• Adjust thresholds based on your network baseline

## Troubleshooting

No packets captured?
→ Ensure you have proper privileges
→ Check interface name (ip link show)

All green but network seems slow?
→ Increase timeout for longer analysis
→ Increase packet count for more samples
            """, "python", line_numbers=False, theme="monokai"))
            raise typer.Exit(0)
        
        # Collect custom parameters
        if "Custom" in mode:
            interface = questionary.text(
                "Network interface (leave blank for auto-detect):",
                style=CUSTOM_STYLE,
            ).ask() or None
            
            timeout = questionary.select(
                "Analysis duration:",
                choices=["5 seconds", "10 seconds", "20 seconds", "30 seconds", "Custom"],
                style=CUSTOM_STYLE,
            ).ask()
            
            if timeout == "Custom":
                timeout = questionary.text(
                    "Enter timeout in seconds (5-300):",
                    validate=lambda x: x.isdigit() and 5 <= int(x) <= 300,
                    style=CUSTOM_STYLE,
                ).ask()
                timeout = int(timeout)
            else:
                timeout = int(timeout.split()[0])
            
            packets = questionary.select(
                "Packet sample size:",
                choices=["50 packets", "100 packets", "200 packets", "500 packets"],
                style=CUSTOM_STYLE,
            ).ask()
            packets = int(packets.split()[0])
        
        console.print()
        return run_analysis(interface, timeout, packets, latency_threshold, loss_threshold)
    
    else:
        # Command-line mode
        return run_analysis(interface, timeout, packets, latency_threshold, loss_threshold)


if __name__ == "__main__":
    app()
