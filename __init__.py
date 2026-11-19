"""AI Vocabulary Tutor for Anki.

This add-on adds an AI vocabulary tutor to Anki's Tools menu.
"""

import os
import sys

_VENDOR_DIR = os.path.join(os.path.dirname(__file__), "vendor")
if _VENDOR_DIR not in sys.path:
    sys.path.insert(0, _VENDOR_DIR)

from aqt import mw
from aqt.qt import QAction, qconnect

from .ui import start_ai_dialog

def register_menu_action() -> None:
    """Register the vocabulary tutor under Anki's Tools menu."""
    action = QAction("AI Vocabulary Tutor", mw)
    qconnect(action.triggered, start_ai_dialog)
    mw.form.menuTools.addAction(action)

register_menu_action()
