from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import MANAGER_CHAT_ID
from state import add_conversation, set_client_to_forward
from .delivery import create_main_menu
def register_contact_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ["contact_manager", "contact_manager_in_menu"])
    def contact_manager(call: CallbackQuery):
        client_id = call.message.chat.id
        bot.send_message(MANAGER_CHAT_ID, f"📲 Клиент {client_id} хочет связаться с вами.")
        bot.send_message(client_id, "📩 Ваш запрос принят. Менеджер свяжется с вами в ближайшее время!")

        add_conversation(client_id, MANAGER_CHAT_ID)

        set_client_to_forward(MANAGER_CHAT_ID, client_id)

        # Show full main menu after confirmation
        bot.send_message(client_id, "🏠 Главное меню. Выберите действие:", reply_markup=create_main_menu())