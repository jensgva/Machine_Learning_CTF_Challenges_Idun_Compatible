"""Shared LLM initialization for the marketplace Research Assistant.

Uses OpenAI gpt-4o-mini.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def search_news(query: str) -> str:
    """Use OpenAI gpt-4o-mini to search for news."""
    client_options = {"api_key": os.environ["OPENAI_API_KEY"]}
    if os.environ.get("OPENAI_BASE_URL"):
        client_options["base_url"] = os.environ["OPENAI_BASE_URL"]
    client = OpenAI(**client_options)
    result = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": query}],
    )
    return result.choices[0].message.content
