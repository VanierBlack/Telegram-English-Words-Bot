# Telegram English Words Bot

This Python script is designed to send a list of English words from an Access database to a specified Telegram chat every day at 12 PM. The script uses the `telebot` library to interact with the Telegram API, `schedule` to manage the timing of the task, and `pyodbc` to connect to the Access database.

## Features

- **Automated Word Sending**: The bot sends a predefined number of words from an Access database to a Telegram chat every day at 12 PM.
- **Registry Management**: The script uses the Windows registry to keep track of the last read index, ensuring that words are not repeated.
- **Environment Variables**: The script uses environment variables to securely store the Telegram API token and chat ID.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- `telebot` library
- `schedule` library
- `pyodbc` library
- `pandas` library
- `python-dotenv` library

You can install the required libraries using the `requirements.txt` file provided in this repository.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/telegram-english-words-bot.git
   cd telegram-english-words-bot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Environment Variables**:
   - Create a `.env` file in the same directory as the script.
   - Add the following lines to the `.env` file:
     ```
     API_TOKEN=your_telegram_api_token
     TO_CHAT_ID=your_telegram_chat_id
     ```

2. **Access Database**:
   - Ensure the Access database file (`English Words.accdb`) is located at `E:\`.
   - The database should contain a table named `ENGLISH_WORDS` with columns `Word`, `Meaning`, and `Spelling`.

3. **Registry Settings**:
   - The script uses the Windows registry to store the last read index. The registry key is created under `HKEY_CURRENT_USER\SOFTWARE\TelegramEnglishBot`.

## Usage

### Running the Script

1. **Run the Script Manually**:
   - Execute the script using Python:
     ```bash
     python your_script_name.py
     ```

### Running as a Service

#### On Windows

1. **Create a Batch File**:
   - Create a batch file (e.g., `run_bot.bat`) with the following content:
     ```batch
     @echo off
     python C:\path\to\your\script\your_script_name.py
     ```

2. **Schedule the Task**:
   - Open Task Scheduler.
   - Create a new task with the following settings:
     - **Trigger**: Daily at 12:00 PM.
     - **Action**: Start a program.
     - **Program/script**: `C:\Windows\System32\cmd.exe`.
     - **Add arguments (optional)**: `/c "C:\path\to\your\script\run_bot.bat"`.

#### On Linux

1. **Create a Systemd Service File**:
   - Create a service file (e.g., `/etc/systemd/system/telegram_english_bot.service`):
     ```ini
     [Unit]
     Description=Telegram English Words Bot
     After=network.target

     [Service]
     ExecStart=/usr/bin/python3 /path/to/your/script/your_script_name.py
     WorkingDirectory=/path/to/your/script/directory
     Restart=always
     User=your_username

     [Install]
     WantedBy=multi-user.target
     ```

2. **Enable and Start the Service**:
   ```bash
   sudo systemctl enable telegram_english_bot.service
   sudo systemctl start telegram_english_bot.service
   ```

## Functions

- **`set_env_key(new_key_name, key_value)`**: Set a new key-value pair in the `.env` file.
- **`send_words(words_list, to_chat_id)`**: Send a list of words to a specified chat ID.
- **`read_access_db(starting_index: int, columns: list)`**: Read words from an Access database starting from a specified index.
- **`manipulate_registry(key_name: str, option: str, new_value: str = None)`**: Manipulate the Windows registry to read or write a value.
- **`build_app()`**: Main function that orchestrates reading from the database, sending words to Telegram, and updating the registry.

## Notes

- The script must be running continuously for the scheduler to work. If you close the script, the scheduled tasks will not run.
- Ensure that the Access database file path and table structure match the script's expectations.
- The script uses the Windows registry to store the last read index. Ensure that the script has the necessary permissions to read and write to the registry.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments

- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [schedule](https://github.com/dbader/schedule)
- [pyodbc](https://github.com/mkleehammer/pyodbc)
- [pandas](https://pandas.pydata.org/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

---

**Author**: [Ahmad Yamen Radwan]  
**Date**: [2024/10/15]  
**Version**: 1.0.0