from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()

# Color mapping for severity badges
SEVERITY_COLORS = {
    "CRITICAL": "bold white on red",
    "HIGH":     "bold white on orange1",
    "MEDIUM":   "bold black on yellow",
    "LOW":      "bold white on green",
}


def _severity_badge(severity: str) -> Text:
    """Returns a colored severity label as a Rich Text object."""
    style = SEVERITY_COLORS.get(severity, "white")
    return Text(f" {severity} ", style=style)


def print_header(filepath: str):
    """Prints the agentsentry banner and the file being scanned."""
    console.print()
    console.print(Panel.fit(
        "[bold cyan]agentsentry[/bold cyan] [dim]— AI Agent Permission Auditor[/dim]",
        border_style="cyan"
    ))
    console.print(f"[dim]Scanning:[/dim] [bold]{filepath}[/bold]\n")


def print_findings(findings: list):
    """Prints all findings in a table."""

    if not findings:
        console.print(Panel(
            "[bold green]✓ No issues found.[/bold green] This agent config looks clean.",
            border_style="green"
        ))
        return

    table = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold dim",
        border_style="dim",
        expand=True
    )

    table.add_column("Severity",  width=12, justify="center")
    table.add_column("Tool",      width=22)
    table.add_column("Finding",   ratio=1)

    for finding in findings:
        severity = finding.get("severity", "LOW")
        tool     = finding.get("tool", "unknown")
        message  = finding.get("message", "")

        table.add_row(
            _severity_badge(severity),
            f"[bold]{tool}[/bold]",
            message
        )

    console.print(table)


def print_summary(score_result: dict, filepath: str):
    """Prints the final risk score panel."""

    level  = score_result["level"]
    score  = score_result["score"]
    color  = score_result["color"]
    counts = score_result["counts"]
    total  = score_result["total"]

    summary = Text()
    summary.append(f"  Risk Score : ", style="dim")
    summary.append(f"{score}/100\n", style=color)

    summary.append(f"  Risk Level : ", style="dim")
    summary.append(f"{level}\n", style=color)

    summary.append(f"  Findings   : ", style="dim")
    summary.append(f"{total} total", style="white")

    if total > 0:
        parts = []
        for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            if counts[sev] > 0:
                parts.append(f"{counts[sev]} {sev}")
        summary.append(f"  ({', '.join(parts)})", style="dim")

    summary.append("\n")
    summary.append(f"  File       : ", style="dim")
    summary.append(filepath, style="dim")

    border_color = {
        "CRITICAL": "red",
        "HIGH":     "orange1",
        "MEDIUM":   "yellow",
        "LOW":      "green"
    }.get(level, "white")

    console.print()
    console.print(Panel(
        summary,
        title=f"[{color}] Audit Result [/{color}]",
        border_style=border_color,
        expand=False
    ))
    console.print()


def print_ai_analysis(ai_result: dict):
    """Prints the AI-powered analysis section."""

    console.print()
    console.rule("[bold cyan]AI Security Analysis[/bold cyan]")

    if not ai_result.get("success"):
        console.print(f"[red]AI analysis failed:[/red] {ai_result.get('error')}")
        return

    if ai_result.get("summary"):
        console.print(Panel(
            ai_result["summary"],
            title="[bold cyan]Executive Summary[/bold cyan]",
            border_style="cyan"
        ))

    if ai_result.get("finding_analysis"):
        console.print(Panel(
            ai_result["finding_analysis"],
            title="[bold yellow]Finding Analysis + Fixes[/bold yellow]",
            border_style="yellow"
        ))

    if ai_result.get("missed_risks"):
        console.print(Panel(
            ai_result["missed_risks"],
            title="[bold orange1]Missed Risks[/bold orange1]",
            border_style="orange1"
        ))

    if ai_result.get("recommendation"):
        console.print(Panel(
            f"[bold]→[/bold] {ai_result['recommendation']}",
            title="[bold green]Overall Recommendation[/bold green]",
            border_style="green"
        ))