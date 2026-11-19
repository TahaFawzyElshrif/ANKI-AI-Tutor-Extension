"""Gemini API integration and Anki vocabulary retrieval."""

from google import genai
from google.genai import types
from anki.collection import Collection

from .config import GEMINI_MODEL, PROMPT_HEAD

def build_prompt(question: str, words: list[str]) -> str:
    """Combine the studied vocabulary and user request into a prompt."""
    vocabulary = ", ".join(words) if words else "No studied vocabulary available."

    return f"Studied vocabulary:\n{vocabulary}\n\nUser request:\n{question}"

def call_gemini_api(

    *,

    question: str,

    api_key: str,

    history: list[dict[str, str]],

    words: list[str],

) -> str:
    """Send the conversation through the official Google Gen AI Python SDK."""

    if not api_key:

        raise RuntimeError("Gemini API key is missing.")

    client = genai.Client(api_key=api_key)

    gemini_history = []

    for message in history:

        role = "model" if message["role"] == "assistant" else "user"

        gemini_history.append(

            types.Content(

                role=role,

                parts=[types.Part.from_text(text=message["content"])],

            )

        )

    chat = client.chats.create(

        model=GEMINI_MODEL,

        history=gemini_history,

        config=types.GenerateContentConfig(

            system_instruction=PROMPT_HEAD,

        ),

    )

    prompt = build_prompt(question, words)

    response = chat.send_message(prompt)

    return response.text or ""

def _get_random_easy_words(col: Collection) -> list[str]:
    """Fetch up to five recently reviewed words from the current deck."""
    deck_id = col.decks.get_current_id()

    return col.db.list(

        """

        SELECT DISTINCT n.sfld

        FROM notes n

        JOIN cards c ON c.nid = n.id

        JOIN revlog r ON r.cid = c.id

        WHERE c.did = ?

          AND r.type IN (0, 1, 2, 3)

          AND r.ease BETWEEN 1 AND 4

          AND n.sfld != ''

        ORDER BY RANDOM()

        LIMIT 5

        """,

        deck_id,

    )
