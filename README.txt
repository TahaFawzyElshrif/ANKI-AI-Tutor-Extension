AI Vocabulary Tutor - Add-on Builder

This builder packages the official Google Gen AI Python SDK inside the Anki add-on.
It targets Anki 26.09.4 / CPython 3.13 / Windows 64-bit.

AI Vocabulary Tutor for Anki
Author: Taha Fawzy Elshrif
GitHub: https://github.com/TahaFawzyElshrif

INSTALL:
1. In Anki, open Tools > Add-ons > Install from file.
2. Select ai_vocabulary_tutor.ankiaddon.
3. Restart Anki.
4. Open Tools > AI Vocabulary Tutor.


Files:
- `__init__.py` — registers the add-on in Anki's Tools menu.
- `config.py` — model name, credential service name, and tutor prompts.
- `credentials.py` — Windows Credential Manager/config storage and API-token dialog.
- `services.py` — Gemini API communication and Anki vocabulary query.
- `chat.py` — chat message rendering and asynchronous request workflow.
- `ui.py` — main chat window and UI event handlers.
