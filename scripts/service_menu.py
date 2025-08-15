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
    """
    Execute a subprocess command given as an argv-style list and wait for it to finish.
    
    If the subprocess exits with a non-zero status, the function catches the resulting
    CalledProcessError and prints an informative message instead of propagating the exception.
    
    Parameters:
        command (List[str]): The command and arguments as a list (argv-style), e.g. ["ls", "-la"].
    
    Returns:
        None
    """
    try:
        subprocess.run(command, check=True)
    except (
        subprocess.CalledProcessError
    ) as exc:  # pragma: no cover - informative output
        print(f"Command failed: {exc}")


def generate_tls() -> None:
    """
    Generate TLS certificates (placeholder).
    
    This is a placeholder implementation that invokes the command runner to simulate TLS certificate
    generation. Replace this function's body with project-specific certificate creation logic
    (e.g., invoking OpenSSL, certbot, or a library) when integrating real TLS setup.
    """
    run_command(["echo", "Generating TLS certificates..."])


def setup_supabase_extras() -> None:
    """
    Install Supabase development "extras" (placeholder).
    
    This function is a placeholder that invokes the command runner with a simulated
    installation message. Replace its body with project-specific installation steps
    for Supabase-related tools or extensions when integrating into a real setup.
    """
    run_command(["echo", "Setting up Supabase extras..."])


def start_langfuse() -> None:
    """
    Start the Langfuse development container.
    
    This is a placeholder implementation that invokes `run_command` with an `echo` command simulating
    the final `docker run` invocation. Replace the body with the real container-start logic as needed.
    """
    run_command(["echo", "docker run -d --name langfuse langfuse/langfuse:latest"])


def start_neo4j() -> None:
    """
    Start the Neo4j development container (placeholder).
    
    This is a placeholder action that invokes the shared `run_command` utility to
    simulate starting a Neo4j Docker container by running an `echo` of the
    `docker run` command. Replace the command with real container orchestration
    logic as needed.
    """
    run_command(["echo", "docker run -d --name neo4j neo4j:latest"])


def start_weaviate() -> None:
    """Start the Weaviate container."""
    run_command(
        ["echo", "docker run -d --name weaviate semitechnologies/weaviate:latest"]
    )


def start_qdrant() -> None:
    """
    Start the Qdrant container (placeholder).
    
    This function is a placeholder that invokes the command runner with an `echo` simulating
    the `docker run` invocation for Qdrant. Replace its implementation with real container
    startup logic when integrating into a project.
    """
    run_command(["echo", "docker run -d --name qdrant qdrant/qdrant:latest"])


def start_postgres() -> None:
    """
    Start a PostgreSQL development container (placeholder).
    
    Invokes the command that would start a PostgreSQL Docker container (name `postgres`, image `postgres:latest`, environment
    variable `POSTGRES_PASSWORD=postgres`). Currently this is simulated via an `echo` command and should be replaced with
    real container startup logic when used in production.
    """
    run_command(
        [
            "echo",
            "docker run -d --name postgres -e POSTGRES_PASSWORD=postgres postgres:latest",
        ]
    )


def start_pgvector() -> None:
    """
    Start a PostgreSQL container with the pgvector extension (placeholder).
    
    This function invokes the command runner with a shell command that simulates starting a
    Postgres container prebuilt with the pgvector extension. It is a placeholder implementation
    that uses an echo'd docker command and can be replaced with real container-start logic.
    """
    run_command(["echo", "docker run -d --name pgvector ankane/pgvector:latest"])


def start_sentry() -> None:
    """
    Start a Sentry container (placeholder).
    
    Invokes run_command with an echo of the `docker run` command for `getsentry/sentry:latest`.
    This function is a placeholder; replace its implementation with real container-start logic as needed.
    """
    run_command(["echo", "docker run -d --name sentry getsentry/sentry:latest"])


def start_openhands() -> None:
    """
    Start the OpenHands container (placeholder).
    
    This function invokes run_command with an `echo` of the Docker run command for the `openhands/openhands:latest` image; it does not actually start a container. Replace the echoed command with real startup logic if you want to launch the container.
    """
    run_command(["echo", "docker run -d --name openhands openhands/openhands:latest"])


def start_archon() -> None:
    """
    Start the Archon container (placeholder).
    
    This function simulates starting the Archon Docker container by invoking the module's
    run_command helper with an `echo` of the `docker run` invocation. It is intended as a
    placeholder and should be replaced with real container-start logic for production use.
    """
    run_command(["echo", "docker run -d --name archon archon/archon:latest"])


def start_agent_zero() -> None:
    """
    Start the Agent-Zero development container.
    
    This is a placeholder that invokes the command runner to simulate starting the `agent-zero`
    container (currently echoes the docker command). Replace with real container-start logic
    as needed.
    """
    run_command(["echo", "docker run -d --name agent_zero agentzero/agent-zero:latest"])


def _build_menu() -> List[MenuItem]:
    """
    Build and return the interactive menu items for the service management TUI.
    
    Each entry is a (label, action) pair where `label` is the displayed menu text and
    `action` is a zero-argument callable executed when the item is selected. The
    menu includes placeholders for TLS generation, Supabase extras installation,
    starting various development service containers, and an "Exit" no-op item.
    
    Returns:
        List[MenuItem]: Ordered list of menu items used by the curses-based UI.
    """
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
    """
    Render a centered text menu in the given curses window and highlight the selected row.
    
    The function clears the screen, centers each menu item's label vertically and horizontally,
    draws them, applies highlight styling to the entry at selected_row_idx using color pair 1,
    and refreshes the display.
    
    Parameters:
        selected_row_idx (int): Index of the menu entry to highlight.
        menu (List[MenuItem]): Sequence of (label, action) pairs; only the label (first element)
            of each tuple is rendered.
    
    Side effects:
        Clears and refreshes the provided curses window.
    """
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
    """
    Run the interactive curses menu loop that lets the user navigate and invoke menu actions.
    
    Displays the menu built by _build_menu, handles Up/Down navigation, and executes the selected item's action when Enter is pressed. Selecting the menu item labeled "Exit" or pressing ESC exits the loop and returns to the caller. The currently running action is shown briefly before returning to the menu and waiting for a key press.
    
    Parameters:
        stdscr (curses.window): The curses window provided by curses.wrapper used for input/output.
    
    Returns:
        None
    """
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
    """
    Initialize the curses-based TUI and run the service menu.
    
    This function is the program entry point: it sets up the curses environment, invokes the interactive menu loop, and ensures terminal state is restored when the menu exits.
    """
    curses.wrapper(run_menu)


if __name__ == "__main__":
    main()
