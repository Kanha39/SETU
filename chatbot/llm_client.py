import os
import time

import requests
from google import genai
from google.genai import errors as genai_errors

from chatbot.config import (
    MODEL_NAME,
    GROQ_MODEL_NAME,
    OPENROUTER_MODEL_NAME,
    SYSTEM_PROMPT,
)

_client = None

# Retried automatically since these are transient (Gemini overloaded / rate
# limited), not something wrong with the request itself.
_RETRYABLE_STATUS_CODES = {429, 503}
_MAX_RETRIES = 3
_BACKOFF_SECONDS = 2  # doubles each retry: 2s, 4s, 8s

_REQUEST_TIMEOUT_SECONDS = 30

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY environment variable is not set. "
                "Set it before calling answer_query()."
            )
        _client = genai.Client(api_key=api_key)
    return _client


def _build_openai_style_messages(user_message: str, context_block: str, history: list) -> list:
    """Groq and OpenRouter both use the OpenAI chat format, unlike Gemini's
    'parts' format -- this builds that shape from the same inputs."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for turn in history[-6:]:
        role = "assistant" if turn["role"] == "model" else "user"
        messages.append({"role": role, "content": turn["text"]})

    prompt = f"PROJECT DATA:\n{context_block}\n\nUSER QUESTION:\n{user_message}"
    messages.append({"role": "user", "content": prompt})
    return messages


def _call_groq(messages: list) -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY environment variable is not set.")

    response = requests.post(
        GROQ_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": GROQ_MODEL_NAME, "messages": messages},
        timeout=_REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def _call_openrouter(messages: list) -> str:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable is not set.")

    response = requests.post(
        OPENROUTER_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": OPENROUTER_MODEL_NAME, "messages": messages},
        timeout=_REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def _call_gemini_only(user_message: str, context_block: str, history: list) -> str:
    """Original Gemini call, unchanged -- kept as the tertiary fallback,
    including its own retry-with-backoff for transient errors."""
    contents = []
    for turn in history[-6:]:
        contents.append({"role": turn["role"], "parts": [{"text": turn["text"]}]})

    prompt = f"PROJECT DATA:\n{context_block}\n\nUSER QUESTION:\n{user_message}"
    contents.append({"role": "user", "parts": [{"text": prompt}]})

    last_error = None
    for attempt in range(_MAX_RETRIES):
        try:
            response = get_client().models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config={"system_instruction": SYSTEM_PROMPT},
            )
            return response.text
        except genai_errors.ServerError as e:
            last_error = e
            status = getattr(e, "code", None) or getattr(e, "status_code", None)
            if status not in _RETRYABLE_STATUS_CODES or attempt == _MAX_RETRIES - 1:
                break
            time.sleep(_BACKOFF_SECONDS * (2 ** attempt))

    raise RuntimeError(
        "Gemini is temporarily unavailable after multiple retries. "
        "This is usually a short-lived issue on Google's side -- try again "
        "in a moment."
    ) from last_error


def call_llm(user_message: str, context_block: str, history: list = None) -> str:
    """Entry point used by chatbot.py. Tries Groq first, then OpenRouter,
    then Gemini (with its existing retry logic), falling through on ANY
    exception from a provider (not just quota/429s), and logs the fallback
    path to console."""
    history = history or []
    messages = _build_openai_style_messages(user_message, context_block, history)

    try:
        result = _call_groq(messages)
        print("[LLM] Answered by Groq.")
        return result
    except Exception as e:
        print(f"[LLM] Groq failed ({e}); falling back to OpenRouter.")

    try:
        result = _call_openrouter(messages)
        print("[LLM] Answered by OpenRouter.")
        return result
    except Exception as e:
        print(f"[LLM] OpenRouter failed ({e}); falling back to Gemini.")

    result = _call_gemini_only(user_message, context_block, history)
    print("[LLM] Answered by Gemini.")
    return result