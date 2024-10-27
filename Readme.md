# EnglishBot README

## Overview

**EnglishBot** is a Python-based Telegram bot designed to help users learn English vocabulary. The bot reads words from an Access database, sends them to a specified chat, and can also create quizzes and delete messages. The project is structured into three main files: `EnglishBot.py`, `Interface.py`, and `libraries.py`.

## Features

- **Send Words**: Automatically sends a list of English words, their meanings, and spellings to a specified Telegram chat.
- **Create Poll**: Generates a quiz with multiple-choice questions based on the words from the database.
- **Delete Message**: Allows the deletion of specific messages sent by the bot.
- **Retrieve Messages**: Retrieves and stores messages from the chat for further analysis.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/EnglishBot.git
   cd EnglishBot
   ```

2. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```
     API_TOKEN=your_telegram_bot_api_token
     TO_CHAT_ID=your_telegram_chat_id
     ```

3. **Install Required Libraries**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

The bot can be controlled via the command line using the `Interface.py` script. Here are the available commands:

- **Send Messages**:
  ```bash
  python Interface.py -s
  ```

- **Create Quiz**:
  ```bash
  python Interface.py -p -q "What is the meaning of 'example'?" -o "Option1" "Option2" "Option3" -a "Option2"
  ```

- **Delete Message**:
  ```bash
  python Interface.py -d 123456789
  ```

- **Retrieve Messages**:
  ```bash
  python Interface.py -m
  ```

### Configuration

- **Database Path**: The path to the Access database file is hardcoded in `EnglishBot.py`. Modify the `FILE_NAME` variable if your database is located elsewhere.
- **Registry Settings**: The bot uses the Windows registry to store and retrieve the starting index for reading words. The registry path is defined in `EnglishBot.py`.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you encounter any bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

For any questions or support, please contact Ahmad Radwan at citum463@gmail.com.

---

**Note**: Ensure that your Telegram bot token and chat ID are kept secure and not shared publicly.