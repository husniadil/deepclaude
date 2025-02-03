from typing import Dict

# API Configuration
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Model Configuration
MODEL_CONFIG: Dict[str, Dict] = {
    "thinking": {
        "name": "deepseek/deepseek-r1",
        "temperature": 0.7,
        "include_reasoning": True,
    },
    "response": {
        "name": "anthropic/claude-3.5-sonnet",
        "temperature": 0.7,
        "max_tokens": 4096,
    },
}

# Buffer Configuration
BUFFER_CONFIG = {"max_size": 1024 * 1024, "chunk_size": 8192, "timeout": 30}  # 1MB

# System Message
DEFAULT_SYSTEM_MESSAGE = "You are a helpful AI assistant who excels at reasoning and responds in Markdown format. For code snippets, you wrap them in Markdown codeblocks with it's language specified."


# Request Headers
def get_default_headers(api_key: str) -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/husniadil/deepclaude",
        "X-Title": "DeepClaude CLI",
    }
