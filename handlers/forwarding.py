from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import MANAGER_CHAT_ID
from state import get_client_to_forward, set_client_to_forward, clear_client_to_forward, ongoing_conversations, has_active_conversations

def register_forwarding_handlers(bot):
    @bot.message_handler(content_types=['text'])
    def forward_message_to_client(message: Message):
        if message.chat.id != MANAGER_CHAT_ID:
            return

        if not has_active_conversations():
            bot.send_message(message.chat.id, "❌ Нет активных диалогов с клиентами.")
            return

        markup = InlineKeyboardMarkup()
        for client_id, convo in ongoing_conversations.items():
            try:
                user = bot.get_chat(client_id)
                markup.add(InlineKeyboardButton(f"{user.first_name} ({client_id})", callback_data=f"client_{client_id}"))
            except Exception as e:
                print(f"Ошибка при получении данных клиента {client_id}: {e}")

        bot.send_message(message.chat.id, "Выберите клиента для общения:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("client_"))
    def forward_message_to_selected_client(call: CallbackQuery):
        client_id = int(call.data.split("_")[1])
        manager_id = call.message.chat.id

        set_client_to_forward(manager_id, client_id)
        bot.send_message(manager_id, "✏️ Введите сообщение, которое хотите отправить клиенту:")

    @bot.message_handler(func=lambda msg: msg.chat.id == MANAGER_CHAT_ID)
    def send_message_to_client(msg: Message):
        client_to_forward = get_client_to_forward(msg.chat.id)
        if client_to_forward:
            bot.send_message(client_to_forward, f"📩 Менеджер: {msg.text}")
            bot.send_message(msg.chat.id, "✅ Сообщение отправлено клиенту.")
            clear_client_to_forward(msg.chat.id)

    @bot.message_handler(content_types=['photo'],
                         func=lambda msg: msg.chat.id == MANAGER_CHAT_ID and 'client_to_forward' in ongoing_conversations.get(msg.chat.id, {}))
    def send_photo_to_client(msg: Message):
        client_to_forward = get_client_to_forward(msg.chat.id)
        if client_to_forward:
            bot.send_photo(client_to_forward, msg.photo[-1].file_id, caption="📷 Сообщение от менеджера")
            bot.send_message(msg.chat.id, "✅ Фото отправлено клиенту.")
            clear_client_to_forward(msg.chat.id)