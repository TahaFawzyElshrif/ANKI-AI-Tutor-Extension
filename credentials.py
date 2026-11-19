
"""Secure storage and input dialog for the Gemini API key."""

import keyring
from typing import Any

from aqt import mw
from aqt.qt import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    qconnect,
)
from aqt.utils import disable_help_button

from .config import KEYRING_SERVICE


def get_gemini_api_key() -> str | None:
    """Retrieve the Gemini API key for the active Anki profile."""

    profile_name = mw.pm.name

    if not profile_name:
        raise RuntimeError("No Anki profile is loaded.")

    return keyring.get_password(KEYRING_SERVICE, profile_name)


def set_gemini_api_key(value: str | None) -> None:
    """Save or remove the Gemini API key for the active Anki profile."""

    profile_name = mw.pm.name

    if not profile_name:
        raise RuntimeError("No Anki profile is loaded.")

    if value:
        keyring.set_password(KEYRING_SERVICE, profile_name, value)
        return

    # Delete the credential only if it exists.
    if keyring.get_password(KEYRING_SERVICE, profile_name) is not None:
        keyring.delete_password(KEYRING_SERVICE, profile_name)


def ask_for_gemini_token(parent: Any) -> str | None:
    """Display a password field and return the entered API token."""

    dialog = QDialog(parent)
    dialog.setWindowTitle("Gemini API Token")
    disable_help_button(dialog)

    layout = QVBoxLayout(dialog)

    label = QLabel(
        "Enter Gemini API Token "
        "(you can get it from Google AI Studio):",
        dialog,
    )
    layout.addWidget(label)

    token_input = QLineEdit(dialog)
    token_input.setPlaceholderText("Enter your Gemini API token here")
    token_input.setEchoMode(QLineEdit.EchoMode.Password)
    layout.addWidget(token_input)

    buttons = QDialogButtonBox(
        QDialogButtonBox.StandardButton.Ok
        | QDialogButtonBox.StandardButton.Cancel,
        parent=dialog,
    )

    qconnect(buttons.accepted, dialog.accept)
    qconnect(buttons.rejected, dialog.reject)
    layout.addWidget(buttons)

    token_input.setFocus()

    if dialog.exec() == QDialog.DialogCode.Accepted:
        token = token_input.text().strip()
        return token or None

    return None
