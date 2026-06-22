import os
from dotenv import load_dotenv
from anthropic import Anthropic
from .config import (
    CLAUDE_DEFAULT_MAX_TOKENS,
    CLAUDE_DEFAULT_MODEL,
    CLAUDE_DEFAULT_TEMPERATURE,
)

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def _parse_anthropic_response(message):
    if message is None:
        return ""

    if hasattr(message, "content"):
        content = message.content
        if isinstance(content, (list, tuple)) and content:
            first = content[0]
            if hasattr(first, "text"):
                return first.text
            if isinstance(first, dict) and "text" in first:
                return first["text"]
            return str(first)

    if hasattr(message, "text"):
        return message.text

    if isinstance(message, dict):
        if "completion" in message:
            return message["completion"]
        if "text" in message:
            return message["text"]

    return ""


def chat(messages, system=None, model=CLAUDE_DEFAULT_MODEL, temperature=CLAUDE_DEFAULT_TEMPERATURE, stop_sequences=None):
    if stop_sequences is None:
        stop_sequences = []

    params = {
        "model": model,
        "max_tokens": CLAUDE_DEFAULT_MAX_TOKENS,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return _parse_anthropic_response(message)


def test_connection(model=CLAUDE_DEFAULT_MODEL):
    """Run a minimal test prompt to verify the Claude connection."""
    messages = []
    add_user_message(messages, "Please reply with the single word OK.")
    response = chat(
        messages,
        system="You are a helpful assistant. Reply with OK.",
        model=model,
        temperature=0.0,
    )
    return (response or "").strip()
