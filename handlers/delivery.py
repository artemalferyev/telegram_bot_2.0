from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
import os

from config import MANAGER_CHAT_ID
from state import add_conversation, set_client_to_forward


def register_delivery_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "delivery")
    def show_delivery_handler(call: CallbackQuery):
        show_delivery(call)

    def show_delivery(call: CallbackQuery, show_image=True):
        if show_image:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))
            with open(os.path.join(base_path, "photo_2025-04-17 12.54.25.jpeg"), "rb") as photo1:
                bot.send_photo(call.message.chat.id, photo1)

        delivery_menu = InlineKeyboardMarkup()
        delivery_menu.add(InlineKeyboardButton("🇺🇸 США", callback_data="delivery_usa"))
        delivery_menu.add(InlineKeyboardButton("🇪🇺 Европа", callback_data="delivery_europe"))
        delivery_menu.add(InlineKeyboardButton("⬅ Назад", callback_data="back_to_main"))

        bot.send_message(call.message.chat.id, "Выберите регион, откуда посылка:", reply_markup=delivery_menu)

    @bot.callback_query_handler(func=lambda call: call.data == "delivery_europe")
    def show_europe_delivery(call: CallbackQuery):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))

        with open(os.path.join(base_path, "photo_2025-04-17 12.53.52.jpeg"), "rb") as photo1, \
             open(os.path.join(base_path, "photo_2025-04-17 12.53.59.jpeg"), "rb") as photo2:
            bot.send_photo(call.message.chat.id, photo1)
            bot.send_photo(call.message.chat.id, photo2,  reply_markup=back_menu)

    back_menu = InlineKeyboardMarkup()
    back_menu.add(InlineKeyboardButton("📞 Связаться с менеджером", callback_data="contact_manager"))
    back_menu.add(InlineKeyboardButton("⬅ Назад к выбору региона", callback_data="delivery_nophoto"))
    back_menu.add(InlineKeyboardButton("⬅ В главное меню", callback_data="back_to_main"))

    @bot.callback_query_handler(func=lambda call: call.data == "delivery_usa")
    def show_usa_delivery(call: CallbackQuery):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))

        with open(os.path.join(base_path, "photo_2025-04-17 13.10.22.jpeg"), "rb") as photo1, \
             open(os.path.join(base_path, "photo_2025-04-17 13.10.28.jpeg"), "rb") as photo2, \
             open(os.path.join(base_path, "photo_2025-04-17 13.10.29.jpeg"), "rb") as photo3:
            bot.send_photo(call.message.chat.id, photo1)
            bot.send_photo(call.message.chat.id, photo2)
            bot.send_photo(call.message.chat.id, photo3, reply_markup=back_menu)

    @bot.callback_query_handler(func=lambda call: call.data == "delivery_nophoto")
    def show_delivery_nophoto(call: CallbackQuery):
        show_delivery(call, show_image=False)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("contact_manager_"))
    def handle_contact_manager(call: CallbackQuery):
        client_id = call.from_user.id
        manager_id = MANAGER_CHAT_ID

        region = "Европа" if call.data == "contact_manager_europe" else "США"
        add_conversation(client_id, manager_id)
        set_client_to_forward(manager_id, client_id)

        bot.send_message(call.message.chat.id, f"Вы обратились к менеджеру. Ожидайте ответа.")