"""Main chat dialog and user interaction handlers."""

from aqt import mw
from aqt.operations import QueryOp
from aqt.qt import (
    QDialog, QHBoxLayout, QVBoxLayout, QGridLayout, QPlainTextEdit,
    QPushButton, QTextBrowser, QLabel, QMessageBox, Qt, qconnect,
)
from aqt.utils import showWarning

from .config import PROMPT_PRACTICE_VOCABULARY, PROMPT_GENERATE_PARAGRAPH, PROMPT_CHOOSE_BETTER_WORD
from .credentials import get_gemini_api_key, set_gemini_api_key, ask_for_gemini_token
from .chat import show_status, send_question
from .services import _get_random_easy_words

def start_ai_dialog() -> None:
    """Load or request the API key, then open the tutor chat."""
    try:

        token = get_gemini_api_key()

    except Exception as exc:

        showWarning(f"Could not access the saved Gemini API key:\n{exc}")

        return

    if not token:

        token = ask_for_gemini_token(mw)

        if not token:

            return

        try:

            set_gemini_api_key(token)

        except Exception as exc:

            showWarning(f"Could not save the Gemini API key:\n{exc}")

            return

    start_chat(token)

def start_chat(token: str) -> None:
    """Build and display the main AI vocabulary tutor chat dialog."""
    dialog = QDialog(mw)

    dialog.setWindowTitle("AI Assistant")

    dialog.resize(760, 640)

    dialog.setMinimumSize(620, 520)

    layout = QVBoxLayout(dialog)

    layout.setContentsMargins(16, 14, 16, 14)

    layout.setSpacing(12)

    messages: list[dict[str, str]] = []

    words_cache: dict[str, list[str] | None] = {"words": None}

    header = QHBoxLayout()

    app_title = QLabel("✦ AI Assistant")

    app_title.setStyleSheet("font-weight: bold; font-size: 16px;")

    header.addWidget(app_title)

    change_token_button = QPushButton("Change Token", dialog)

    new_chat_button = QPushButton("New Chat", dialog)

    header.addWidget(change_token_button)

    header.addWidget(new_chat_button)

    header.addStretch()

    layout.addLayout(header)

    welcome = QVBoxLayout()

    welcome.setSpacing(5)

    welcome_title = QLabel("What would you like to practice?")

    welcome_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

    welcome_title.setStyleSheet("font-size: 18px; font-weight: bold;")

    welcome_subtitle = QLabel("Choose an activity or ask me anything.")

    welcome_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

    welcome.addSpacing(12)

    welcome.addWidget(welcome_title)

    welcome.addWidget(welcome_subtitle)

    welcome.addSpacing(12)

    layout.addLayout(welcome)

    chat_view = QTextBrowser(dialog)

    chat_view.setOpenExternalLinks(True)

    chat_view.setPlainText(

        "Your AI study assistant is ready.\n"

        "Choose an activity above or type your question below."

    )

    layout.addWidget(chat_view, 1)

    suggestions_layout = QGridLayout()

    suggestions_layout.setSpacing(8)

    suggestions = [

        ("Practice Vocabulary", PROMPT_PRACTICE_VOCABULARY, 0, 0),

        ("Generate Paragraph", PROMPT_GENERATE_PARAGRAPH, 0, 1),

        ("Choose the Better Word", PROMPT_CHOOSE_BETTER_WORD, 1, 0),

    ]

    question = QPlainTextEdit(dialog)

    question.setPlaceholderText("Ask anything...")

    question.setMaximumHeight(85)

    question.setTabChangesFocus(True)

    def set_prompt(prompt: str) -> None:

        question.setPlainText(prompt)

        question.setFocus()

    for title, prompt, row, col in suggestions:

        button = QPushButton(title, dialog)

        button.setMinimumHeight(60)

        button.setToolTip(prompt)

        qconnect(

            button.clicked,

            lambda checked=False, p=prompt: set_prompt(p),

        )

        suggestions_layout.addWidget(button, row, col)

    layout.addLayout(suggestions_layout)

    input_row = QHBoxLayout()

    input_row.setSpacing(8)

    send_button = QPushButton("Send", dialog)

    send_button.setMinimumWidth(85)

    send_button.setMinimumHeight(65)

    input_row.addWidget(question, 1)

    input_row.addWidget(send_button)

    layout.addLayout(input_row)

    def change_token() -> None:

        nonlocal token

        confirmation = QMessageBox.question(

            dialog,

            "Change Gemini API Token",

            "Are you sure you want to change the Gemini API token?",

            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,

            QMessageBox.StandardButton.No,

        )

        if confirmation != QMessageBox.StandardButton.Yes:

            return

        new_token = ask_for_gemini_token(dialog)

        if new_token:

            try:

                set_gemini_api_key(new_token)

            except Exception as exc:

                showWarning(f"Could not save the Gemini API key:\n{exc}", parent=dialog)

                return

            token = new_token

    qconnect(change_token_button.clicked, change_token)

    def new_chat() -> None:

        confirmation = QMessageBox.question(

            dialog,

            "New Chat",

            "Are you sure you want to start a new conversation?",

            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,

            QMessageBox.StandardButton.No,

        )

        if confirmation != QMessageBox.StandardButton.Yes:

            return

        messages.clear()

        words_cache["words"] = None

        chat_view.clear()

        chat_view.setPlainText(

            "Your AI study assistant is ready.\n"

            "Choose an activity above or type your question below."

        )

        question.clear()

        show_status(chat_view, "Getting your studied vocabulary...")

        send_button.setEnabled(False)

        new_chat_button.setEnabled(False)

        def on_new_words_loaded(words: list[str]) -> None:

            words_cache["words"] = words

            if not words:

                show_status(

                    chat_view,

                    "No studied vocabulary found. Continuing without vocabulary context.",

                )

            send_button.setEnabled(True)

            new_chat_button.setEnabled(True)

        def on_new_words_error(exc: Exception) -> None:

            words_cache["words"] = []

            show_status(chat_view, f"Could not retrieve vocabulary: {exc}")

            send_button.setEnabled(True)

            new_chat_button.setEnabled(True)

        QueryOp(

            parent=dialog,

            op=_get_random_easy_words,

            success=on_new_words_loaded,

        ).failure(on_new_words_error).run_in_background()

    qconnect(new_chat_button.clicked, new_chat)

    def handle_send() -> None:

        user_text = question.toPlainText().strip()

        if not user_text:

            return

        question.clear()

        send_button.setEnabled(False)

        new_chat_button.setEnabled(False)

        send_question(

            text=user_text,

            token=token,

            messages=messages,

            chat_view=chat_view,

            dialog=dialog,

            send_button=send_button,

            words_cache=words_cache,

            new_chat_button=new_chat_button,

        )

    qconnect(send_button.clicked, handle_send)

    dialog.exec()
