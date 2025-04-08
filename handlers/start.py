from telebot.types import Message
from keyboards import get_inline_menu

def register_start_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message: Message):
        bot.send_message(
            message.chat.id,
            (
                "Здравствуйте! \n\n"
                "Я - бот-помощник байер-сервиса KUPIDON, созданный для вашего удобства. "
                "Я отвечу на все ваши вопросы! \n\n"
                "Байер-сервис KUPIDON помогает осуществлять покупки желаемых товаров из США, Европы, "
                "а также ювелирных украшений из Дубая. \n\n"
                "Почему шопинг с KUPIDON — это лучший выбор? Вот 5 причин: \n\n"
                "- Адекватная наценка; \n"
                "- Бесплатные замеры; \n"
                "- Только оригинальные брендовые вещи с гарантией качества и подлинности; \n"
                "- Индивидуальный подход к каждому клиенту; \n"
                "- Выгодные условия доставки. \n\n"
                "Выберите интересующий раздел или напишите сообщение ниже 🔻"
            ),
            reply_markup=get_inline_menu()
        )