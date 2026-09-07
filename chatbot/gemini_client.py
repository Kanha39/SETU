import os

from google import genai

from chatbot.config import MODEL_NAME, SYSTEM_PROMPT

_client = None


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
    response = get_client().models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={"system_instruction": SYSTEM_PROMPT},
    )
    return response.text
