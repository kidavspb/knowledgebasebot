import os

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from init import *
import hashlib


# Функция для генерации MD5-хеша на основе пути
def generate_hash(path):
    return hashlib.md5(path.encode()).hexdigest()


# Функция для генерации клавиатуры на основе файлов и папок
def generate_keyboard(path):
    items = os.listdir(path)
    keyboard = InlineKeyboardMarkup()

    # Кнопки для папок и файлов
    for item in items:
        full_path = os.path.join(path, item)
        item_hash = generate_hash(full_path)  # Генерируем хеш для каждого элемента
        path_hash_map[item_hash] = full_path  # Сохраняем соответствие хеша и пути

        if os.path.isdir(full_path):
            keyboard.add(InlineKeyboardButton(f'📁 {item}', callback_data=f'folder:{item_hash}'))
        elif item.endswith('.txt'):
            keyboard.add(InlineKeyboardButton(f'📄 {item[:-4]}', callback_data=f'file:{item_hash}'))

    # Кнопка "Назад", если мы не в корне
    if path != KNOWLEDGE_BASE_PATH:
        parent_hash = generate_hash(os.path.dirname(path))
        path_hash_map[parent_hash] = os.path.dirname(path)
        keyboard.add(InlineKeyboardButton('⬅️ Назад', callback_data=f'back:{parent_hash}'))

    return keyboard


def can_access(message):
    if message.chat.type != 'private':
        return False
    elif message.chat.id in admins:
        return True
    elif message.chat.id in current_users_manager.get_data():
        if current_users_manager.get_data()[message.chat.id] != message.chat.username:
            current_users_manager.add_data(message.chat.id, message.chat.username)
        return True
    elif message.chat.username in new_users_manager.get_data():
        current_users_manager.add_data(message.chat.id, message.chat.username)
        new_users_manager.del_data(message.chat.username)
        return True
    else:
        return False
