import time
import commands

from utils import *


# Команда /start
@bot.message_handler(commands=['start'], func=lambda message: can_access(message))
def start(message):
    chat_id = message.chat.id
    logging.info(f"Start message from user @{message.from_user.username} ({chat_id})")
    user_paths[chat_id] = KNOWLEDGE_BASE_PATH  # Устанавливаем начальный путь
    keyboard = generate_keyboard(KNOWLEDGE_BASE_PATH)
    bot.send_message(chat_id, 'Выберите раздел:', reply_markup=keyboard)


# Обработка кнопок
@bot.callback_query_handler(func=lambda call: can_access(call.message))
def callback_handler(call):
    chat_id = call.message.chat.id
    data = call.data

    # Если нажата папка
    if data.startswith('folder:'):
        folder_hash = data.split(':', 1)[1]
        folder_path = path_hash_map.get(folder_hash)

        if folder_path:
            logging.info(f'User @{call.message.chat.username} ({chat_id}) selected folder: {folder_path}')
            user_paths[chat_id] = folder_path  # Обновляем путь пользователя
            keyboard = generate_keyboard(folder_path)
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Выберите раздел:",
                                  reply_markup=keyboard)
        else:
            logging.warning(
                f'Folder path not found for hash: {folder_hash}')  # TODO: добавить какое-то уведомление пользователю (answer?)
            bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
            start(call.message)

    # Если нажата тема (файл)
    elif data.startswith('file:'):
        file_hash = data.split(':', 1)[1]
        file_path = path_hash_map.get(file_hash)

        if file_path:
            logging.info(f'User @{call.message.chat.username} ({chat_id}) selected file: {file_path}')
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            bot.send_message(chat_id=chat_id, text=content, parse_mode='HTML',
                             reply_markup=InlineKeyboardMarkup().add(
                                 InlineKeyboardButton('❌ Закрыть', callback_data='close')))
        else:
            logging.warning(f'File path not found for hash: {file_hash}')
            bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
            start(call.message)

    # Если нажата кнопка "Назад"
    elif data.startswith('back:'):
        parent_hash = data.split(':', 1)[1]
        parent_path = path_hash_map.get(parent_hash)

        if parent_path:
            logging.info(
                f'User @{call.message.chat.username} ({chat_id}) pressed back button, navigating to: {parent_path}')
            user_paths[chat_id] = parent_path  # Обновляем путь пользователя
            keyboard = generate_keyboard(parent_path)
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Выберите раздел:",
                                  reply_markup=keyboard)
        else:
            logging.warning(f'Parent path not found for hash: {parent_hash}')
            bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
            start(call.message)

    elif data == 'close':
        logging.info(f'Close button pressed by user @{call.message.chat.username} ({chat_id})')
        bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)


while True:
    try:
        bot.polling(none_stop=True)
        logging.info("Bot running..")
    except Exception as e:
        logging.error(e)
        bot.stop_polling()
        time.sleep(15)
        logging.info("Running again!")
