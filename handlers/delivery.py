from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
import os

def register_delivery_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "delivery")
    def show_delivery(call: CallbackQuery):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))

        with open(os.path.join(base_path, "photo_2025-01-17 15.47.06.jpeg"), "rb") as photo1, \
             open(os.path.join(base_path, "photo_2025-01-17 15.47.09.jpeg"), "rb") as photo2:
            bot.send_photo(call.message.chat.id, photo1)
            bot.send_photo(call.message.chat.id, photo2)

        delivery_menu = InlineKeyboardMarkup()
        delivery_menu.add(InlineKeyboardButton("🇺🇸 США", callback_data="delivery_usa"))
        delivery_menu.add(InlineKeyboardButton("🇪🇺 Европа", callback_data="delivery_europe"))
        delivery_menu.add(InlineKeyboardButton("⬅ Назад", callback_data="back_to_main"))

        bot.send_message(call.message.chat.id, "Выберите регион доставки:", reply_markup=delivery_menu)

    @bot.callback_query_handler(func=lambda call: call.data == "delivery_europe")
    def show_europe_delivery(call: CallbackQuery):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))

        with open(os.path.join(base_path, "photo_2025-01-17 15.47.11.jpeg"), "rb") as photo1, \
             open(os.path.join(base_path, "photo_2025-01-17 15.47.13.jpeg"), "rb") as photo2:
            bot.send_photo(call.message.chat.id, photo1)
            bot.send_photo(call.message.chat.id, photo2)

        back_menu = InlineKeyboardMarkup()
        back_menu.add(InlineKeyboardButton("⬅ Назад", callback_data="delivery"))

        bot.send_message(call.message.chat.id, "⬅ Вернуться назад", reply_markup=back_menu)

    @bot.callback_query_handler(func=lambda call: call.data == "delivery_usa")
    def show_usa_delivery(call: CallbackQuery):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))

        with open(os.path.join(base_path, "photo_2025-01-17 15.47.16.jpeg"), "rb") as photo1, \
             open(os.path.join(base_path, "photo_2025-01-17 15.47.18.jpeg"), "rb") as photo2:
            bot.send_photo(call.message.chat.id, photo1)
            bot.send_photo(call.message.chat.id, photo2)

        back_menu = InlineKeyboardMarkup()
        back_menu.add(InlineKeyboardButton("⬅ Назад", callback_data="delivery"))

        bot.send_message(call.message.chat.id, "⬅ Вернуться назад", reply_markup=back_menu)