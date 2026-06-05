import argparse
import sys
from agentwatch.parser import load_agent_config
from agentwatch.analyzers.permissions import analyze_permissions
from agentwatch.analyzers.combinations import analyze_combinations
from agentwatch.analyzers.scoring import calculate_score
from agentwatch.report import print_header, print_findings, print_summary
from rich.console import Console

console = Console()


def cmd_audit(args):
    """Runs the full audit pipeline on a given config file."""

    filepath = args.file

    # Step 1 — Print the header banner
    print_header(filepath)

    # Step 2 — Load and parse the config file
    try:
        config = load_agent_config(filepath)
    except (FileNotFoundError, ValueError) as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

    # Step 3 — Run both analyzers and combine findings
    permission_findings   = analyze_permissions(config)
    combination_findings  = analyze_combinations(config)
    all_findings          = permission_findings + combination_findings

    # Step 4 — Calculate risk score from all findings
    score_result = calculate_score(all_findings)

    # Step 5 — Print findings table
    print_findings(all_findings)

    # Step 6 — Print final summary panel
    print_summary(score_result, filepath)

    # Exit with code 1 if HIGH or CRITICAL so CI/CD pipelines can catch it
    if score_result["level"] in ["HIGH", "CRITICAL"]:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog="agentwatch",
        description="Audit AI agent config files for dangerous permissions and risky tool combinations."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- "audit" subcommand ---
    audit_parser = subparsers.add_parser(
        "audit",
        help="Audit an agent config file"
    )
    audit_parser.add_argument(
        "file",
        help="Path to the agent config file (.yaml, .yml, or .json)"
    )
    audit_parser.set_defaults(func=cmd_audit)

    # Parse and dispatch
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()