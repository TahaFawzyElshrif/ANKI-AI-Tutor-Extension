# AI Vocabulary Tutor for Anki

An AI-powered Anki add-on that helps learners reinforce and actively use previously studied English vocabulary through contextual practice and AI-assisted conversations.

## Overview

The main purpose of this add-on is to help users remember and actively use previously studied English vocabulary.

Instead of simply memorizing definitions, learners are encouraged to recall, understand, and use vocabulary in different contexts through AI-assisted exercises and conversations.

The AI assistant complements Anki's existing learning and review system; it does not replace the normal studying process.

## Related Project

This add-on provides functionality similar to the AI tutor integrated into my modified Anki version.

For more details about the original implementation and its features, see:

[Anki AI Tutor – Modified Anki Version](https://github.com/TahaFawzyElshrif/Anki-AI-Tutor-)

## Download

Download the latest release from the GitHub Releases page:

**[Download AI Vocabulary Tutor](../../releases)**

## Installation

1. Open Anki.
2. Navigate to **Tools → Add-ons → Install from file**.
3. Select `ai_vocabulary_tutor.ankiaddon`.
4. Restart Anki.
5. Open **Tools → AI Vocabulary Tutor**.

## Technical Implementation

### Dependency Management

The official Google Gen AI Python SDK and its required dependencies are not included in Anki's standard Python environment.

This can cause dependency-related issues when running the add-on.

To address this, the required packages are bundled with the add-on rather than requiring users to install Python dependencies manually.

The implementation uses dependency freezing and a bundled dependency directory (`vendor/`) to provide the required packages within the extension.

### Target Environment

| Component | Target |
|---|---|
| Anki Version | 26.09.4 |
| Python Runtime | CPython 3.13 |
| Operating System | Windows 64-bit |
| AI SDK | Google Gen AI Python SDK |

**Compatibility Note:** The add-on has been tested on Windows with Anki 26.09.4. Compatibility with other Anki versions and operating systems has not been verified.

## Project Structure

| File | Description |
|---|---|
| `__init__.py` | Registers the add-on in Anki's Tools menu. |
| `config.py` | Contains the model name, credential service name, and tutor prompts. |
| `credentials.py` | Handles Windows Credential Manager, configuration storage, and the API token dialog. |
| `services.py` | Manages Gemini API communication and Anki vocabulary queries. |
| `chat.py` | Handles chat message rendering and asynchronous request workflows. |
| `ui.py` | Implements the main chat window and UI event handlers. |
| `vendor/` | Contains bundled Python dependencies required by the add-on. |
| `vendors.7z` | Dependency archive included in the release package. |

## Updating the Add-on

If an update is released, for example, to upgrade dependencies such as `google-genai` or `keyring`, or to change the Gemini model name, follow these steps:

1. Download the latest extension package from GitHub Releases.
2. Extract the updated package if required.
3. Replace the existing extension files with the updated files.
4. Restart Anki.

If you encounter any issues during the update, please open an issue in the repository.

## Common Issues

### Installation Takes a Long Time

**Expected behavior:** The installation process may take a few minutes, particularly when bundled dependencies are being extracted or initialized.

**Solution:** Allow the process to finish. Avoid interrupting it unnecessarily.

### Cannot Remove the Extension

If the extension cannot be removed through the usual method:

1. Open Anki.
2. Navigate to **Tools → Add-ons → View Files**.
3. Locate the extension directory.
4. Remove the extension files or disable the add-on through the Add-ons Manager.

## Security & Anki Integration

### Credential Protection

The add-on uses Python's `keyring` library to securely store the user's Google Gemini API key through the Windows Credential Manager.

- API keys are not hardcoded or bundled with the add-on.
- Credentials are stored locally using the operating system's credential storage mechanism.
- Users can provide their own API key through the add-on's interface.

### Native Anki Integration

The add-on is designed to preserve Anki's existing architecture and user experience.

- Integrates directly into Anki's Tools menu.
- Uses Anki's existing Python and Qt environment.
- Reuses Anki's vocabulary and collection data.
- Maintains a modular structure while following Anki's add-on conventions.
- Does not require a separate application or a modified Anki installation.

## Limitations

- **Operating System:** Tested on Windows only.
- **Anki Version:** Tested with Anki 26.09.4.
- **Python Runtime:** Targets CPython 3.13.
- **Package Compatibility:** Compatibility may depend on the installed Anki version and bundled dependency versions.
- **External Service:** AI functionality depends on the availability of the Google Gemini API.

## Disclaimer

This software has been tested, but it is not guaranteed to be free of bugs or unexpected issues.

It is provided "AS IS", without warranties of any kind. Use it at your own risk.

The author is not responsible for any damage, data loss, or unexpected behavior resulting from the use of this software.

## Author

**Taha Fawzy Elshrif**

- GitHub: [@TahaFawzyElshrif](https://github.com/TahaFawzyElshrif)
- Project: AI Vocabulary Tutor for Anki

---

*Built to make vocabulary learning more active, contextual, and effective.*