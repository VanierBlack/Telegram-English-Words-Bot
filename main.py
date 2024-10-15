import telebot
import schedule
import time
import winreg
import pandas as pd
import pyodbc
import os
from dotenv import set_key, load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve API token and chat ID from environment variables
API_TOKEN = os.getenv("API_TOKEN")
TO_CHAT_ID = os.getenv("TO_CHAT_ID")

# Constants # You can change them to what ever you want

# Access File Name
FILE_NAME = "for example: English Words.accdb"
# SUB Key to be Opened or Created in the registry for to contain the app variable

SUBKEY_APP = "for example: TelegramEnglishBot"

# APP variable name 
APP_NAME = "for example: EnglishBotWords"

# The Maximum Number of rows to read
MAXIMUM_READ_WORDS = 5

# Constants # Don't Change
MAIN_REGISTRY = winreg.HKEY_CURRENT_USER
MAIN_PATH = "SOFTWARE"

# Initialize the Telegram bot
bot = telebot.TeleBot(API_TOKEN)

def set_env_key(new_key_name, key_value):
    """
    Set a new key-value pair in the .env file.

    :param new_key_name: The name of the new key.
    :param key_value: The value to be set for the new key.
    """
    set_key(".env", new_key_name, key_value)

def send_words(words_list, to_chat_id):
    """
    Send a list of words to a specified chat ID.

    :param words_list: A list of tuples containing word, meaning, and spelling.
    :param to_chat_id: The chat ID to send the message to.
    :return: True if the message was sent successfully, False otherwise.
    """
    full_message = "\n".join(f"{word[0]}: {word[1]}: {word[2]}" for word in words_list)
    try:
        sent_message = bot.send_message(to_chat_id, full_message)
        if sent_message.message_id:
            print(f"Message sent successfully! Message ID: {sent_message.message_id}")
            return True
        else:
            print("Message was not sent successfully.")
            return False
    except telebot.apihelper.ApiException as e:
        print(f"Failed to send message: {e}")
        return False

def read_access_db(starting_index: int, columns: list):
    """
    Read words from an Access database starting from a specified index.

    :param starting_index: The index to start reading from.
    :return: A DataFrame containing the words, meanings, and spellings.
    """
    path_to_access_file = f"E:\\{FILE_NAME}"
    connection_string = rf'Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={path_to_access_file};'
    
    with pyodbc.connect(connection_string) as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM ENGLISH_WORDS ORDER BY Word")
        words_rows = [tuple(row) for row in cursor.fetchall()[starting_index: starting_index + MAXIMUM_READ_WORDS]]

    return pd.DataFrame(words_rows, columns=columns)

def manipulate_registry(key_name: str, option: str, new_value: str = None):
    """
    Manipulate the Windows registry to read or write a value.

    :param key_name: The name of the registry key.
    :param option: The operation to perform ('read' or 'write').
    :param new_value: The new value to write (only required for 'write' operation).
    :return: The value read from the registry or 0 if the operation was successful.
    """
    full_path = f"{MAIN_PATH}\\{SUBKEY_APP}"
    try:
        with winreg.OpenKeyEx(MAIN_REGISTRY, full_path, 0, winreg.KEY_READ | winreg.KEY_WRITE) as opened_registry:
            if option == "read":
                return int(winreg.QueryValueEx(opened_registry, key_name)[0])
            elif option == "write" and new_value is not None:
                winreg.SetValueEx(opened_registry, key_name, 0, winreg.REG_SZ, new_value)
                return 0
    except FileNotFoundError:
        with winreg.CreateKey(MAIN_REGISTRY, full_path) as new_key:
            winreg.SetValueEx(new_key, key_name, 0, winreg.REG_SZ, new_value)
            return 0

def build_app():
    # Main execution
    starting_index = manipulate_registry(APP_NAME, "read")

    # Columns parameters should be passed to the function as a list to identify the tublar data using DataFrame
    words = read_access_db(starting_index, ["Word", "Meaning", "Spelling"])

    response_state = send_words(words.values, TO_CHAT_ID)
    if response_state:
        starting_index += MAXIMUM_READ_WORDS
        manipulate_registry(APP_NAME, "write", str(starting_index))

    else:
        pass

if __name__ == "__main__":
    while True:
        schedule.every().day.at("12:00").do(build_app)
        time.sleep(1)