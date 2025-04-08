from telebot.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import MANAGER_CHAT_ID
from state import (
    ongoing_conversations, add_conversation, get_manager_for_client,
    set_client_to_forward, get_client_to_forward, clear_client_to_forward,
    has_active_conversations
)

def register_messaging_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "contact_manager")
    def contact_manager(call: CallbackQuery):
        client_id = call.message.chat.id

        bot.send_message(
            MANAGER_CHAT_ID,
            f"📲 Клиент {client_id} хочет связаться с вами. Напишите им в ближайшее время."
        )
        bot.send_message(client_id, "📩 Ваш запрос принят. Менеджер свяжется с вами в ближайшее время!")

        add_conversation(client_id, MANAGER_CHAT_ID)

        back_to_conversion_menu = InlineKeyboardMarkup()
        back_to_conversion_menu.add(InlineKeyboardButton("⬅ Назад", callback_data="conversion"))

        bot.edit_message_reply_markup(client_id, call.message.message_id, reply_markup=back_to_conversion_menu)

    @bot.callback_query_handler(func=lambda call: call.data == "contact_manager_in_menu")
    def contact_manager_from_menu(call: CallbackQuery):
        client_id = call.message.chat.id

        bot.send_message(MANAGER_CHAT_ID, f"📲 Клиент {client_id} хочет связаться с вами.")
        bot.send_message(client_id, "📩 Ваш запрос принят. Менеджер свяжется с вами в ближайшее время!")

        add_conversation(client_id, MANAGER_CHAT_ID)

        back_to_main_menu = InlineKeyboardMarkup()
        back_to_main_menu.add(InlineKeyboardButton("⬅ Назад", callback_data="back_to_main"))

        bot.edit_message_reply_markup(client_id, call.message.message_id, reply_markup=back_to_main_menu)

    @bot.message_handler(commands=['clients'], func=lambda msg: msg.chat.id == MANAGER_CHAT_ID)
    def show_active_clients(msg: Message):
        print("Processing /clients command...")

        if not has_active_conversations():
            bot.send_message(msg.chat.id, "❌ Нет активных клиентов.")
            return

        markup = InlineKeyboardMarkup()

        for client_id in ongoing_conversations:
            try:
                bot.send_message(client_id, "📩 Менеджер доступен для общения!")

                user = bot.get_chat(client_id)
                markup.add(
                    InlineKeyboardButton(f"{user.first_name} ({client_id})", callback_data=f"client_{client_id}")
                )
            except Exception as e:
                print(f"Ошибка при получении данных о клиенте {client_id}: {e}")

        bot.send_message(msg.chat.id, "Выберите клиента для общения:", reply_markup=markup)

    @bot.message_handler(content_types=['text', 'photo', 'video', 'voice', 'document'],
                         func=lambda message: message.chat.id == MANAGER_CHAT_ID)
    def handle_manager_message(message: Message):
        if not ongoing_conversations:
            bot.send_message(message.chat.id, "❌ Нет активных диалогов с клиентами.")
            return

        client_id = get_client_to_forward(message.chat.id)

        if client_id is None:
            bot.send_message(message.chat.id, "❌ Не найден активный разговор с этим клиентом.")
            return

        try:
            if message.text:
                bot.send_message(client_id, f"📩 Менеджер: {message.text}")
            elif message.photo:
                bot.send_photo(client_id, message.photo[-1].file_id, caption="📷 Сообщение от менеджера")
            elif message.voice:
                bot.send_voice(client_id, message.voice.file_id, caption="🎙 Голосовое сообщение от менеджера")
            elif message.document:
                bot.send_document(client_id, message.document.file_id, caption="📂 Документ от менеджера")

            clear_client_to_forward(message.chat.id)

        except Exception as e:
            print(f"❌ Ошибка при отправке клиенту {client_id}: {e}")

    @bot.message_handler(content_types=['text', 'photo', 'video', 'voice', 'document'])
    def catch_all(message: Message):
        ongoing_conversations[message.chat.id] = {'manager_id': MANAGER_CHAT_ID, 'client_id': message.chat.id}

    @bot.callback_query_handler(func=lambda call: call.data.startswith("client_"))
    def forward_message_to_selected_client(call: CallbackQuery):
        client_id = int(call.data.split("_")[1])
        manager_id = call.message.chat.id

        set_client_to_forward(manager_id, client_id)
        bot.send_message(manager_id, "Введите сообщение для клиента:")

    @bot.message_handler(content_types=['photo'],
                         func=lambda msg: msg.chat.id in ongoing_conversations and 'client_to_forward' in
                                          ongoing_conversations[msg.chat.id])
    def send_photo_to_client(msg: Message):
        client_to_forward = ongoing_conversations[msg.chat.id].get('client_to_forward')

        if client_to_forward:
            bot.send_photo(client_to_forward, msg.photo[-1].file_id, caption="📷 Сообщение от менеджера")
            bot.send_message(msg.chat.id, "✅ Фото отправлено клиенту.")
            del ongoing_conversations[msg.chat.id]['client_to_forward']