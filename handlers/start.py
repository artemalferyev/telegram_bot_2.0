import json
import os

USER_FILE = "users.json"

def load_user_ids():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_user_ids(user_ids):
    with open(USER_FILE, "w") as f:
        json.dump(list(user_ids), f)

user_ids = load_user_ids()

from telebot.types import Message
from keyboards import get_inline_menu

def register_start_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message: Message):
        username = message.from_user.username or message.from_user.first_name or "друг"
        first_name = message.from_user.first_name or "друг"
        print(f"✅ Команда /start вызвана пользователем: {username} (ID: {message.from_user.id})")
        user_id = message.from_user.id
        if user_id not in user_ids:
            user_ids.add(user_id)
            save_user_ids(user_ids)
        bot.send_message(
            message.chat.id,
            (
                f"Здравствуйте, {first_name}! 🤍\n\n"
                "Я — бот-помощник байер-сервиса KUPIDON, созданный для вашего удобства.\n\n"
                "KUPIDON помогает заказывать желанные товары из США, Европы, а также ювелирные украшения из Дубая.\n\n"
                "Почему шопинг с KUPIDON — это отличный выбор?\n\n "
                "Вот 5 причин:\n\n"
                "- Адекватна наценка\n"
                "- Только оригинальные бренды с гарантией подлинности\n"
                "- Индивидуальный подход к каждому клиенту\n"
                "- Выгодные условия доставки\n"
                "- Постоянная поддержка и консультации на каждом этапе заказа\n\n"
                "Выберите нужный раздел ниже или нажмите кнопку, чтобы связаться с менеджером 🔻\n"
            ),
            reply_markup=get_inline_menu()
        )