## Overview

The DeepClaude CLI provides a simple yet powerful command-line interface that leverages OpenRouter to access both DeepSeek R1 and Claude models. It allows you to harness the combined power of DeepSeek R1's reasoning and Claude's capabilities directly from your terminal, with a convenient chat-like interface and command history.

## Features

**Dual Model Integration** - Utilizes DeepSeek R1 for reasoning and Claude 3.5 Sonnet for final responses

**Interactive Interface** - Chat-like interface with command history (accessible with up/down arrows)

**Real-time Streaming** - See both the reasoning process and final responses as they're generated

**Markdown Support** - Beautifully formatted responses with proper code highlighting

**Secure** - API key management through environment variables with no data storage

## Installation

1. Ensure you have Python 3.7 or higher installed

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Environment Setup

Set your OpenRouter API key as an environment variable:

```bash
export OPENROUTER_API_KEY="your-openrouter-api-key"
```

Alternatively, you can create a `.env` file in the CLI directory with:
```
OPENROUTER_API_KEY=your-openrouter-api-key
```

### Model Configuration

The CLI uses the following default model configuration:

- **Thinking Process**: DeepSeek R1 (temperature: 0.7)
- **Final Response**: Claude 3.5 Sonnet (temperature: 0.7, max tokens: 4096)

## Usage

### Basic Usage

Start the interactive CLI:

```bash
python deepclaude.py
```

This will start an interactive session where you can chat with the AI. Features include:
- Command history navigation (up/down arrows)
- Markdown-formatted responses
- Real-time streaming of both thinking and final responses
- Exit commands: Type 'exit', 'quit', or press Ctrl+D

## Examples

```bash
Welcome to DeepClaude CLI!
Type 'exit' or press Ctrl+D to quit

You: hi

Thinking:
Okay, the user said "hi". That's pretty straightforward. I should respond in a friendly and welcoming manner. Since I need to use Markdown and codeblocks when necessary, but "hi" doesn't require any code. Let me
make sure I follow the guidelines: keep responses helpful, use Markdown for code, but otherwise just natural conversation. Maybe say hello, acknowledge their greeting, and offer assistance. Let me check if that's
appropriate. Yep, that seems right. No need for any complex reasoning here. Just be polite and open. Hello! How can I assist you today? 😊

Response:
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                    Hello! 👋                                                                                                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Welcome! I'm here to help you with any questions or tasks you might have. Feel free to ask me anything - whether it's about coding, analysis, general information, or any other topic you'd like to explore.

You:

Goodbye!
```
