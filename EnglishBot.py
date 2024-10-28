from libraries import *

# Load environment variables from the .env file
load_dotenv()

# Retrieve API token and chat ID from environment variables
API_TOKEN = os.getenv("API_TOKEN")
TO_CHAT_ID = os.getenv("TO_CHAT_ID")

# Constants # You can change them to what ever you want
FILE_NAME = "English Words.accdb"
SUBKEY_APP = "TelegramEnglishBot"
APP_NAME = "EnglishBotWords"
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
    full_message = "\n".join(f"{word[0]} - {word[1]} - {word[2]}" for word in words_list)
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

def read_access_db(starting_index):
    """
    Read words from an Access database starting from a specified index.

    :param starting_index: The index to start reading from.
    :return: A DataFrame containing the words, meanings, and spellings.
    """
    path_to_access_file = f"E:\\{FILE_NAME}"
    connection_string = rf'Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={path_to_access_file};'
    
    with pyodbc.connect(connection_string) as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM ENGLISH_WORDS")
        words_rows = [tuple(row) for row in cursor.fetchall()[starting_index: starting_index + MAXIMUM_READ_WORDS]]

    return pd.DataFrame(words_rows, columns=["Word", "Meaning", "Spelling"])

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

def main():
    # Main execution
    starting_index = manipulate_registry(APP_NAME, "read")
    words = read_access_db(starting_index)

    response_state = send_words(words.values, TO_CHAT_ID)
    if response_state:
        starting_index += MAXIMUM_READ_WORDS
        manipulate_registry(APP_NAME, "write", str(starting_index))
    else:
        pass

def find_correct_answer(options, answer):
    for index, element in enumerate(options):
        if element == answer:
            return index

def CreatePoll(poll_question, poll_options, correct_answer):
    message_id = bot.send_poll(TO_CHAT_ID, poll_question, poll_options, type = "quiz", correct_option_id = find_correct_answer(poll_options, correct_answer[0]))

def DeleteMessage(message_id):
    if bot.delete_message(TO_CHAT_ID, message_id):
        print("Message Deleted Successfully")

def InitiateMessagesTracking():
    # Function to handle all incoming messages
    @bot.message_handler(func=lambda message: True) # Handle all messages
    def handle_message(message):
        chat_id = -1 * (message.chat.id) if (message.chat.id < 0) else (message.chat.id)
        message_text = message.text

        # Optionally process the message
        print(f"Received message from chat ID: {chat_id}, text: {message_text}")
        # Save message data (example: to a JSON file)
        message_data = {
                'chat_id': message.chat.id,
                'message_id': message.message_id,
                'text': message.text,
                'date': message.date,
                'from_user': {
                    'id': message.from_user.id,
                    'first_name': message.from_user.first_name,
                    'last_name': message.from_user.last_name,
                    'username': message.from_user.username
                },
                'chat': {
                    'id': message.chat.id,
                    'type': message.chat.type,
                    'title': message.chat.title,
                    'username': message.chat.username
                }
            }
        with open("messages.json", "a") as f:
            json.dump(message_data, f)
            f.write('\n') # Add a newline for better readability
        
    @bot.poll_answer_handler(func = lambda poll: True)
    def receive(poll_answer: telebot.types.PollAnswer):
        print(poll_answer.user)
        
    bot.polling(none_stop = True, interval = 0)

    


