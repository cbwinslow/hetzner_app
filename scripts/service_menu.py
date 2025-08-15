#!/usr/bin/env python3
"""Simple TUI menu for managing development services.

This interactive menu provides shortcuts for common setup tasks such as
TLS certificate generation and launching optional service containers.
Each option invokes a placeholder shell command that can be replaced with
project-specific logic in the future.
"""

from __future__ import annotations

import curses
import subprocess
from typing import Callable, List, Tuple

MenuItem = Tuple[str, Callable[[], None]]


def run_command(command: List[str]) -> None:
    """Execute a shell command and wait for it to complete."""
    try:
        subprocess.run(command, check=True)
    except (
        subprocess.CalledProcessError
    ) as exc:  # pragma: no cover - informative output
        print(f"Command failed: {exc}")


def generate_tls() -> None:
    """Placeholder for TLS certificate generation."""
    run_command(["echo", "Generating TLS certificates..."])


def setup_supabase_extras() -> None:
    """Placeholder for installing Supabase extras."""
    run_command(["echo", "Setting up Supabase extras..."])


def start_langfuse() -> None:
    """Start the Langfuse container."""
    run_command(["echo", "docker run -d --name langfuse langfuse/langfuse:latest"])


def start_neo4j() -> None:
    """Start the Neo4j container."""
    run_command(["echo", "docker run -d --name neo4j neo4j:latest"])


def start_weaviate() -> None:
    """Start the Weaviate container."""
    run_command(
        ["echo", "docker run -d --name weaviate semitechnologies/weaviate:latest"]
    )


def start_qdrant() -> None:
    """Start the Qdrant container."""
    run_command(["echo", "docker run -d --name qdrant qdrant/qdrant:latest"])


def start_postgres() -> None:
    """Start the PostgreSQL container."""
    run_command(
        [
            "echo",
            "docker run -d --name postgres -e POSTGRES_PASSWORD=postgres postgres:latest",
        ]
    )


def start_pgvector() -> None:
    """Start a PostgreSQL container with the pgvector extension."""
    run_command(["echo", "docker run -d --name pgvector ankane/pgvector:latest"])


def start_sentry() -> None:
    """Start the Sentry container."""
    run_command(["echo", "docker run -d --name sentry getsentry/sentry:latest"])


def start_openhands() -> None:
    """Start the OpenHands container."""
    run_command(["echo", "docker run -d --name openhands openhands/openhands:latest"])


def start_archon() -> None:
    """Start the Archon container."""
    run_command(["echo", "docker run -d --name archon archon/archon:latest"])


def start_agent_zero() -> None:
    """Start the Agent-Zero container."""
    run_command(["echo", "docker run -d --name agent_zero agentzero/agent-zero:latest"])


def _build_menu() -> List[MenuItem]:
    return [
        ("Generate TLS certificates", generate_tls),
        ("Install Supabase extras", setup_supabase_extras),
        ("Start Langfuse container", start_langfuse),
        ("Start Neo4j container", start_neo4j),
        ("Start Weaviate container", start_weaviate),
        ("Start Qdrant container", start_qdrant),
        ("Start PostgreSQL container", start_postgres),
        ("Start pgvector container", start_pgvector),
        ("Start Sentry container", start_sentry),
        ("Start OpenHands container", start_openhands),
        ("Start Archon container", start_archon),
        ("Start Agent-Zero container", start_agent_zero),
        ("Exit", lambda: None),
    ]


def draw_menu(
    stdscr: curses.window, selected_row_idx: int, menu: List[MenuItem]
) -> None:
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, item in enumerate(menu):
        x = w // 2 - len(item[0]) // 2
        y = h // 2 - len(menu) // 2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, item[0])
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, item[0])
    stdscr.refresh()


def run_menu(stdscr: curses.window) -> None:
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    menu = _build_menu()
    current_row = 0
    while True:
        draw_menu(stdscr, current_row, menu)
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key in {curses.KEY_ENTER, ord("\n")}:
            label, action = menu[current_row]
            if label == "Exit":
                break
            stdscr.clear()
            stdscr.addstr(0, 0, f"Running: {label}\n")
            stdscr.refresh()
            action()
            stdscr.addstr(2, 0, "Press any key to return to menu")
            stdscr.getch()
        elif key == 27:  # ESC key
            break


def main() -> None:
    curses.wrapper(run_menu)


if __name__ == "__main__":
    main()
