"""Shared LLM initialization for the victim Financial Assistant.

Uses OpenAI gpt-4o-mini.
"""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def get_llm(temperature: float = 0) -> ChatOpenAI:
    """Return a ChatOpenAI instance for gpt-4o-mini."""
    client_options = {
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "temperature": temperature,
        "max_tokens": 2048,
    }
    if os.getenv("OPENAI_BASE_URL"):
        client_options["base_url"] = os.environ["OPENAI_BASE_URL"]
    return ChatOpenAI(
        **client_options,
    )
