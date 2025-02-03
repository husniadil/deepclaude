from typing import Dict, List, Optional, Generator
import json
import requests
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from config import (
    DEFAULT_SYSTEM_MESSAGE,
    API_URL,
    MODEL_CONFIG,
    BUFFER_CONFIG,
    get_default_headers,
)


class ApiClient:
    def __init__(self, api_key: str, console: Console):
        self.api_key = api_key
        self.console = console
        self.default_headers = get_default_headers(api_key)

    def _make_streaming_request(
        self,
        url: str,
        payload: Dict,
        max_buffer: int = BUFFER_CONFIG["max_size"],
        chunk_size: int = BUFFER_CONFIG["chunk_size"],
        timeout: int = BUFFER_CONFIG["timeout"],
    ) -> Generator[tuple[Dict, Live, int], None, None]:
        """Make a streaming request to the API with error handling."""
        try:
            response = requests.post(
                url,
                headers=self.default_headers,
                json=payload,
                stream=True,
                timeout=timeout,
            )
            response.raise_for_status()

            content = ""
            buffer_size = 0

            with Live("", refresh_per_second=10) as live:
                for line in response.iter_lines(chunk_size=chunk_size):
                    if not line:
                        continue

                    try:
                        line_str = line.decode("utf-8")
                        if not line_str.startswith("data: "):
                            continue

                        data = json.loads(line_str[6:])
                        yield data, live, buffer_size

                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        self.console.print(
                            f"[yellow]Warning: Error processing chunk: {str(e)}[/yellow]"
                        )
                        continue

        except requests.Timeout:
            self.console.print("[red]Error: Request timed out[/red]")
            return None
        except requests.RequestException as e:
            self.console.print(f"[red]Error making request: {str(e)}[/red]")
            return None
        except Exception as e:
            self.console.print(f"[red]Unexpected error: {str(e)}[/red]")
            return None

    def get_thinking_response(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """Get thinking/reasoning response from DeepSeek-R1 model."""
        if not messages:
            self.console.print("[red]Error: No messages provided[/red]")
            return None

        # Add system message to the beginning of messages
        messages_with_system = [
            {"role": "system", "content": DEFAULT_SYSTEM_MESSAGE}
        ] + messages

        payload = {
            "model": MODEL_CONFIG["thinking"]["name"],
            "messages": messages_with_system,
            "stream": True,
            "include_reasoning": MODEL_CONFIG["thinking"]["include_reasoning"],
            "temperature": MODEL_CONFIG["thinking"]["temperature"],
        }

        thinking = ""
        buffer_size = 0
        max_buffer = 1024 * 1024

        try:
            for data, live, current_buffer_size in self._make_streaming_request(
                API_URL, payload
            ):
                choice = data.get("choices", [{}])[0]
                content = None

                if "message" in choice:
                    content = choice["message"].get("reasoning")
                elif "delta" in choice:
                    delta_msg = choice["delta"].get("message", {})
                    content = delta_msg.get("reasoning")

                    if not content:
                        content = choice["delta"].get("reasoning")

                    if not content:
                        content = choice["delta"].get("content")

                if content:
                    new_buffer_size = buffer_size + len(content)
                    if new_buffer_size > max_buffer:
                        self.console.print(
                            "[yellow]Warning: Response too large, truncating...[/yellow]"
                        )
                        break

                    thinking += content
                    buffer_size = new_buffer_size
                    live.update(Markdown(thinking))

            return thinking if thinking else None

        except Exception as e:
            self.console.print(f"[red]Error during streaming: {str(e)}[/red]")
            return thinking if thinking else None

    def get_final_response(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """Get final response from Claude 3.5 Sonnet model."""
        if not messages:
            self.console.print("[red]Error: No messages provided[/red]")
            return None

        # Add system message to the beginning of messages
        messages_with_system = [
            {"role": "system", "content": DEFAULT_SYSTEM_MESSAGE}
        ] + messages

        payload = {
            "model": MODEL_CONFIG["response"]["name"],
            "messages": messages_with_system,
            "stream": True,
            "temperature": MODEL_CONFIG["response"]["temperature"],
            "max_tokens": MODEL_CONFIG["response"]["max_tokens"],
        }

        content = ""
        buffer_size = 0
        max_buffer = 1024 * 1024

        try:
            for data, live, current_buffer_size in self._make_streaming_request(
                API_URL, payload
            ):
                choice = data.get("choices", [{}])[0]
                delta = choice.get("delta", {})

                if content_chunk := delta.get("content"):
                    new_buffer_size = buffer_size + len(content_chunk)
                    if new_buffer_size > max_buffer:
                        self.console.print(
                            "[yellow]Warning: Response too large, truncating...[/yellow]"
                        )
                        break

                    content += content_chunk
                    buffer_size = new_buffer_size
                    live.update(Markdown(content))

            return content if content else None

        except Exception as e:
            self.console.print(f"[red]Error during streaming: {str(e)}[/red]")
            return content if content else None
