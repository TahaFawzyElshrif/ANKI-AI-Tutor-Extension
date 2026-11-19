"""Conversation message rendering and asynchronous chat workflow."""

import html

from aqt.operations import QueryOp
from aqt.qt import QDialog, QPushButton, QTextBrowser

from .services import _get_random_easy_words, call_gemini_api

def add_message(

    chat_view: QTextBrowser,

    messages: list[dict[str, str]],

    role: str,

    content: str,

) -> None:
    """Append a chat message to the conversation history and display it."""
    messages.append({"role": role, "content": content})

    sender = "You" if role == "user" else "AI"

    safe_content = html.escape(content).replace("\n", "<br>")

    chat_view.append(f"<p><b>{sender}</b><br>{safe_content}</p>")

def show_status(chat_view: QTextBrowser, message: str) -> None:
    """Display a status message in the chat view."""
    safe_message = html.escape(message).replace("\n", "<br>")

    chat_view.append(f"<p><i>{safe_message}</i></p>")

def send_question(

    *,

    text: str,

    token: str,

    messages: list[dict[str, str]],

    chat_view: QTextBrowser,

    dialog: QDialog,

    send_button: QPushButton,

    words_cache: dict[str, list[str] | None],

    new_chat_button: QPushButton,

) -> None:
    """Retrieve vocabulary context and submit the user's question to Gemini."""
    add_message(chat_view, messages, "user", text)

    show_status(chat_view, "Getting your studied vocabulary...")

    def on_words_loaded(words: list[str]) -> None:

        words_cache["words"] = words

        if not words:

            show_status(

                chat_view,

                "No studied vocabulary found. Continuing without vocabulary context.",

            )

        history = messages[:-1].copy()

        show_status(chat_view, "Waiting for Gemini...")

        operation = QueryOp(

            parent=dialog,

            op=lambda _col: call_gemini_api(

                question=text,

                api_key=token,

                history=history,

                words=words,

            ),

            success=lambda response: on_gemini_done(

                response, messages, chat_view, send_button, new_chat_button

            ),

        )

        operation.failure(

            lambda exc: on_gemini_error(

                exc, chat_view, send_button, new_chat_button

            )

        ).without_collection().run_in_background()

    def on_words_error(exc: Exception) -> None:

        show_status(chat_view, f"Could not retrieve vocabulary: {exc}")

        send_button.setEnabled(True)

        new_chat_button.setEnabled(True)

    if words_cache["words"] is not None:

        on_words_loaded(words_cache["words"] or [])

    else:

        QueryOp(

            parent=dialog,

            op=_get_random_easy_words,

            success=on_words_loaded,

        ).failure(on_words_error).run_in_background()

def on_gemini_done(

    response: str,

    messages: list[dict[str, str]],

    chat_view: QTextBrowser,

    send_button: QPushButton,

    new_chat_button: QPushButton,

) -> None:
    """Display Gemini's response and re-enable chat controls."""
    if response:

        add_message(chat_view, messages, "assistant", response)

    else:

        show_status(chat_view, "Gemini returned an empty response.")

    send_button.setEnabled(True)

    new_chat_button.setEnabled(True)

def on_gemini_error(

    exc: Exception,

    chat_view: QTextBrowser,

    send_button: QPushButton,

    new_chat_button: QPushButton,

) -> None:
    """Display the Gemini error and re-enable chat controls."""
    show_status(chat_view, f"Gemini error: {exc}")

    send_button.setEnabled(True)

    new_chat_button.setEnabled(True)
