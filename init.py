import logging
import telebot

from secret import *
from jsonhandling import ListManager

# Создаем бота
bot = telebot.TeleBot(TOKEN)
BOT_ID = bot.get_me().id

# Указываем путь к базе знаний
KNOWLEDGE_BASE_PATH = 'knowledge_base'

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(module)s - %(levelname)s: %(lineno)d - %(message)s",
    handlers=[
        logging.FileHandler(logfile_name),
        logging.StreamHandler()
    ],
    datefmt='%d/%b %H:%M:%S',
)

# Словарь для хранения текущего пути пользователя и соответствий хешей
user_paths = {}
path_hash_map = {}

current_users_manager = ListManager("users/current_users.json")
new_users_manager = ListManager("users/new_users.json", key_as_int=False)
logging.info(f"Data loaded from files")