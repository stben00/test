import telebot
from dotenv import load_dotenv
import os

from new_tg.db import get_cities, save_users, get_user_with_cities, get_user_by_chat_id

load_dotenv()
token = os.getenv("TOKEN")

bot = telebot.TeleBot(token)

ADMIN_ID = 2028373354

user_state = {}


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Как тебя зовут?")
    user_state[message.chat.id] = {"step": "name"}

@bot.message_handler(commands=["get_info"])
def all_info(message):
    user = get_user_by_chat_id(message.chat.id)
    if not user:
        bot.send_message(message.chat.id, "Ты ещё не зарегистрирован. Напиши /start")
        return
    name, age, city = user
    bot.send_message(message.chat.id, f"Имя: {name}\nВозраст: {age}\nГород: {city}")

@bot.message_handler(commands=["users"])
def users(message):
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, "Нет доступа")
        return

    users_list = get_user_with_cities()

    if not users_list:
        bot.send_message(message.chat.id, "Пользователей пока нет")
        return

    text = ""

    for name, age, city in users_list:
        text += f"{name} {age} {city}\n"

    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def handle(message):
    chat_id = message.chat.id
    state = user_state.get(chat_id)

    if not state:
        bot.send_message(chat_id, "Напиши /start")
        return

    if state["step"] == "name":
        state["name"] = message.text
        state["step"] = "age"
        bot.send_message(chat_id, "Какой у тебя возраст?")

    elif state["step"] == "age":
        if not message.text.isdigit():
            bot.send_message(chat_id, "Возраст должен быть числом")
            return

        state["age"] = int(message.text)
        state["step"] = "city"

        cities = get_cities()

        text = "Выберите город:\n"
        for city_id, city_name in cities:
            text += f"{city_id}. {city_name}\n"

        bot.send_message(chat_id, text)

    elif state["step"] == "city":
        if not message.text.isdigit():
            bot.send_message(chat_id, "Отправь номер города")
            return

        city_id = int(message.text)

        save_users(chat_id, state["name"], state["age"], city_id)

        bot.send_message(chat_id, "Пользователь добавлен")
        del user_state[chat_id]


if __name__ == "__main__":
    bot.polling(non_stop=True)