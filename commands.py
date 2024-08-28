from init import *


@bot.message_handler(commands=['help'], func=lambda message: message.from_user.id in admins)
def help(message):
    text = "*Список команд:*\n\n" \
           "/start — выйти в корень базы знаний\n" \
           "/help — помощь\n\n" \
           "`/add\_member @username` — выдать пользователю доступ к базе знаний\n" \
           "`/delete\_member @username` — забрать у пользователя доступ к базе знаний\n\n" \
           "/show\_members — показать список пользователей с доступом к базе знаний\n"
    bot.send_message(message.from_user.id, text, parse_mode="MarkdownV2")
    logging.info(f"Sent help message to user @{message.from_user.username}")


@bot.message_handler(commands=['add_member'], func=lambda message: message.from_user.id in admins)
def add_member(message):
    splitted_text = message.text.split()
    if len(splitted_text) == 2 and splitted_text[1].startswith("@"):
        new_username = splitted_text[1][1:]
        new_users_manager.add_data(new_username, -1)
        logging.info(f"Member @{new_username} added to new_users.json by @{message.from_user.username}")
        bot.send_message(message.from_user.id, f"Пользователь @{new_username} добавлен")
    else:
        bot.send_message(message.from_user.id, "Неверный формат команды: `/add\_member @username`",
                         parse_mode="MarkdownV2")


@bot.message_handler(commands=['delete_member'], func=lambda message: message.from_user.id in admins)
def delete_member(message):
    splitted_text = message.text.split()
    if len(splitted_text) == 2 and splitted_text[1].startswith("@"):
        old_username = splitted_text[1][1:]
        new_users_manager.del_data(old_username)
        for id, username in current_users_manager.get_data().items():
            if username == old_username:
                current_users_manager.del_data(id)
                break
        logging.info(f"Member @{old_username}\" deleted from users by @{message.from_user.username}")
        bot.send_message(message.from_user.id, f"Пользователь @{old_username} удален")
    else:
        bot.send_message(message.from_user.id, "Неверный формат команды: `/delete\_member @username`",
                         parse_mode="MarkdownV2")


@bot.message_handler(commands=['show_members'], func=lambda message: message.from_user.id in admins)
def show_members(message):
    text = "*Список пользователей:*\n\n"
    for member_id, member_username in current_users_manager.get_data().items():
        text += f"{member_id}:{member_username}\n"

    text += "\nИ ожидают добавления:\n"
    for member_username, _ in new_users_manager.get_data().items():
        text += f"@{member_username}\n"
    bot.send_message(message.from_user.id, text, parse_mode="MarkdownV2")
    logging.info(f"Sent users list to user @{message.from_user.username}")
