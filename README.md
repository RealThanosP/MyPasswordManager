# Password Manager

A Python-based desktop Password Manager featuring a modern GUI (customtkinter), secure password generation, and encrypted vault storage.

**Status:** Work in Progress. (Currently restructuring database and encryption modules).

## Features

*   **Password Generator:** Create strong, customizable passwords (length, numbers, symbols, readability).
*   **Multiple Vaults:** Organize accounts into different "vaults" (encrypted containers).
*   **Secure Storage:** Accounts (Username, Password, Service) are encrypted and stored locally.
*   **Modern GUI:** Built with `customtkinter` for a clean, dark-mode friendly interface.

## Prerequisites

*   Python 3.10 or higher
*   Git

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Thanos-2005/MyPasswordManager
    cd MyPasswordManager
    ```

2.  **Create a virtual environment (Recommended):**
    
    *   **Linux/macOS:**
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        python -m venv .venv
        .venv\Scripts\activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(If `requirements.txt` is missing, install manually: `pip install customtkinter Pillow pyperclip`)*

## Usage

1.  **Activate your virtual environment** (if not already active).
2.  **Run the application:**
    ```bash
    python main.py
    ```

## Project Structure

*   `main.py`: Application entry point.
*   `gui.py`: Defines the GUI classes.
*   `PassGen.py`: Password generation logic.
*   `database.py`: SQLite database interactions.
*   `encryption.py`: Encryption/Decryption logic.
*   `config.json` & `config.py`: Configuration settings.

## Development Notes

*   **Security Warning:** The current encryption implementation is custom and has known weaknesses. It is being refactored for better security. Do not use for high-value credentials yet.
*   **Database:** Uses `sqlite3` locally (`database.db`).

## License

[MIT](https://choosealicense.com/licenses/mit/)