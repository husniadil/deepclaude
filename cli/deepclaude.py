#!/usr/bin/env python3

import os
import sys
from typing import List, Dict, Optional
import typer
from rich.console import Console
from prompt_toolkit import PromptSession
from dotenv import load_dotenv
from api_client import ApiClient
from config import DEFAULT_SYSTEM_MESSAGE

# Initialize Rich console for pretty output
console = Console()

# Load environment variables
load_dotenv()


def initialize_api_client() -> Optional[ApiClient]:
    """Initialize the API client with environment variables."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        console.print(
            "[red]Error: OPENROUTER_API_KEY environment variable not set[/red]"
        )
        return None
    return ApiClient(api_key, console)


def handle_conversation(api_client: ApiClient, messages: List[Dict[str, str]]) -> bool:
    """Handle a single conversation turn with the API."""
    # Display static thinking header and get thinking response
    console.print("\n[bold blue]Thinking:[/bold blue]")
    thinking = api_client.get_thinking_response(messages)

    if thinking:
        # Add thinking to conversation
        messages.append(
            {"role": "assistant", "content": f"<thinking>\n{thinking}\n</thinking>"}
        )

        # Display static response header and get final response
        console.print("\n[bold green]Response:[/bold green]")
        response = api_client.get_final_response(messages)

        if response:
            messages.append({"role": "assistant", "content": response})
            console.print()  # Add newline after response
            return True

    return False


def main():
    """Main CLI interface with improved error handling and type hints."""
    # Initialize API client
    api_client = initialize_api_client()
    if not api_client:
        sys.exit(1)

    # Initialize session without history storage
    session = PromptSession()

    # Initialize conversation with system message
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": DEFAULT_SYSTEM_MESSAGE}
    ]

    # Display welcome message
    console.print("[bold green]Welcome to DeepClaude CLI![/bold green]")
    console.print("Type 'exit' or press Ctrl+D to quit\n")

    while True:
        try:
            # Get user input
            user_input = session.prompt("You: ").strip()

            # Handle exit commands
            if user_input.lower() in ["exit", "quit"]:
                break

            # Skip empty input
            if not user_input:
                continue

            # Add user message to conversation
            messages.append({"role": "user", "content": user_input})

            # Handle the conversation turn
            handle_conversation(api_client, messages)

        except (EOFError, KeyboardInterrupt):
            break
        except Exception as e:
            console.print(f"\n[red]Error: {str(e)}[/red]")

    console.print("\n[bold green]Goodbye![/bold green]")


if __name__ == "__main__":
    typer.run(main)
