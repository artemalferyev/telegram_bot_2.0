from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import MANAGER_CHAT_ID
from state import add_conversation

def register_contact_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ["contact_manager", "contact_manager_in_menu"])
    def contact_manager(call: CallbackQuery):
        client_id = call.message.chat.id
        bot.send_message(MANAGER_CHAT_ID, f"📲 Клиент {client_id} хочет связаться с вами.")
        bot.send_message(client_id, "📩 Ваш запрос принят. Менеджер свяжется с вами в ближайшее время!")
        add_conversation(client_id, MANAGER_CHAT_ID)

        back_menu = InlineKeyboardMarkup()
        back_menu.add(InlineKeyboardButton("⬅ Назад", callback_data="back_to_main"))
        bot.edit_message_reply_markup(client_id, call.message.message_id, reply_markup=back_menu)