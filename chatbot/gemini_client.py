import os
import time
 
from google import genai
from google.genai import errors as genai_errors
 
from chatbot.config import MODEL_NAME, SYSTEM_PROMPT
 
_client = None
 
# Retried automatically since these are transient (Gemini overloaded / rate
# limited), not something wrong with the request itself.
_RETRYABLE_STATUS_CODES = {429, 503}
_MAX_RETRIES = 3
_BACKOFF_SECONDS = 2  # doubles each retry: 2s, 4s, 8s
 
 
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
 
 
def call_gemini(user_message: str, context_block: str) -> str:
    prompt = f"PROJECT DATA:\n{context_block}\n\nUSER QUESTION:\n{user_message}"
 
    last_error = None
    for attempt in range(_MAX_RETRIES):
        try:
            response = get_client().models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
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