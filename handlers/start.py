from telebot.types import Message
from keyboards import get_inline_menu

def register_start_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message: Message):
        first_name = message.from_user.first_name or "друг"
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