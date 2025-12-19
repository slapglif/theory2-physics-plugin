#!/bin/bash
# Theory2 Plugin - Trace mathlib4 for LeanDojo
# This is a long-running operation (~1 hour on fast hardware)
set -e

MATHLIB_COMMIT="${1:-v4.3.0-rc2}"
THEORY2_DIR="${THEORY2_DIR:-$HOME/theory2}"
LEAN_DOJO_CACHE="${LEAN_DOJO_CACHE_DIR:-$HOME/.cache/lean_dojo}"

echo "=== LeanDojo mathlib4 Tracing ==="
echo "Commit: $MATHLIB_COMMIT"
echo "Cache: $LEAN_DOJO_CACHE"
echo "Theory2: $THEORY2_DIR"
echo ""
echo "This will take approximately 1 hour and requires 32GB+ RAM."
echo "Starting in 5 seconds... (Ctrl+C to cancel)"
sleep 5

# Use theory2 venv if available
if [ -f "$THEORY2_DIR/.venv/bin/python" ]; then
    PYTHON="$THEORY2_DIR/.venv/bin/python"
    echo "Using Python: $PYTHON"
else
    PYTHON="python3"
    echo "Using system Python: $PYTHON"
fi

# Run tracing
export LEAN_DOJO_CACHE_DIR="$LEAN_DOJO_CACHE"

$PYTHON << EOF
import os
import sys
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

console = Console()

console.print("[bold cyan]Starting LeanDojo mathlib4 tracing...[/bold cyan]")
console.print(f"[dim]Cache directory: {os.environ.get('LEAN_DOJO_CACHE_DIR', '~/.cache/lean_dojo')}[/dim]")

try:
    from lean_dojo import LeanGitRepo, trace

    console.print("[yellow]Creating LeanGitRepo for mathlib4...[/yellow]")
    repo = LeanGitRepo(
        "https://github.com/leanprover-community/mathlib4",
        "$MATHLIB_COMMIT"
    )
    console.print(f"[green]Repo created: {repo}[/green]")

    console.print("[yellow]Starting tracing (this takes ~1 hour)...[/yellow]")
    console.print("[dim]Progress will be logged by LeanDojo...[/dim]")

    traced_repo = trace(repo)

    console.print(f"[bold green]Tracing complete![/bold green]")
    console.print(f"[green]Traced repo path: {traced_repo.repo_path}[/green]")

except Exception as e:
    console.print(f"[bold red]Error: {e}[/bold red]")
    import traceback
    traceback.print_exc()
    sys.exit(1)

console.print("[bold green]mathlib4 is now cached for LeanDojo![/bold green]")
EOF

echo ""
echo "Tracing complete!"
