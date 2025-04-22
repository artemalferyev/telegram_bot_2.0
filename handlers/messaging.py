from telebot.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import MANAGER_CHAT_ID
from state import (
    ongoing_conversations, add_conversation, get_manager_for_client,
    set_client_to_forward, get_client_to_forward,
    has_active_conversations
)

def register_messaging_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "contact_manager")
    @bot.callback_query_handler(func=lambda call: call.data == "contact_manager_in_menu")
    def contact_manager(call):
        client_id = call.from_user.id
        client_name = f"{call.from_user.first_name} {call.from_user.last_name or ''}".strip()

        add_conversation(client_id, MANAGER_CHAT_ID)
        set_client_to_forward(MANAGER_CHAT_ID, client_id)

        if MANAGER_CHAT_ID is None:
            bot.answer_callback_query(call.id, "❌ Менеджер временно недоступен. Попробуйте позже или обратитесь в поддержку.")
            return

        back_to_main_menu = InlineKeyboardMarkup()
        back_to_main_menu.add(InlineKeyboardButton("⬅ Назад", callback_data="back_to_main"))

        bot.answer_callback_query(call.id, "Менеджер скоро с вами свяжется!")

        bot.send_message(
            MANAGER_CHAT_ID,
            f"👤 Новый запрос от клиента: [{client_name}](tg://user?id={client_id})\n\n"
            f"ID: `{client_id}`",
            parse_mode="Markdown"
        )

    @bot.message_handler(commands=['clients'], func=lambda msg: msg.chat.id == MANAGER_CHAT_ID)
    def show_active_clients(msg: Message):
        print("Processing /clients command...")

        if not has_active_conversations(msg.chat.id):
            bot.send_message(msg.chat.id, "❌ Нет активных клиентов.")
            return

        markup = InlineKeyboardMarkup()

        for client_id in ongoing_conversations:
            try:
                user = bot.get_chat(client_id)
                markup.add(
                    InlineKeyboardButton(f"{user.first_name} ({client_id})", callback_data=f"client_{client_id}")
                )
            except Exception as e:
                print(f"Ошибка при получении данных о клиенте {client_id}: {e}")

        bot.send_message(msg.chat.id, "Выберите клиента для общения:", reply_markup=markup)

    @bot.message_handler(content_types=['text', 'photo', 'video', 'voice', 'document', 'video_note'],
                         func=lambda message: message.chat.id == MANAGER_CHAT_ID)
    def handle_manager_message(message: Message):
        if not has_active_conversations(message.chat.id):
            bot.send_message(message.chat.id, "❌ Нет активных диалогов с клиентами.")
            return

        client_id = get_client_to_forward(message.chat.id)

        print(f"Manager state: {ongoing_conversations.get(message.chat.id)}")

        if client_id is None:
            bot.send_message(message.chat.id, "❌ Не найден активный разговор с этим клиентом.")
            return

        try:
            if message.text:
                bot.send_message(client_id, message.text)
                print(f"Forwarded manager message to client {client_id}")
            elif message.photo:
                bot.send_photo(client_id, message.photo[-1].file_id, caption=message.caption)
                print(f"Forwarded manager photo to client {client_id}")
            elif message.voice:
                bot.send_voice(client_id, message.voice.file_id, caption=message.caption)
                print(f"Forwarded manager voice message to client {client_id}")
            elif message.video:
                bot.send_video(client_id, message.video.file_id, caption=message.caption)
                print(f"Forwarded manager video to client {client_id}")
            elif message.video_note:
                bot.send_video_note(client_id, message.video_note.file_id)
                print(f"Forwarded manager video note to client {client_id}")

        except Exception as e:
            print(f"❌ Ошибка при отправке клиенту {client_id}: {e}")

    @bot.message_handler(content_types=['text', 'photo', 'video', 'voice', 'document', 'video_note'])
    def catch_all(message: Message):
        client_id = message.chat.id

        if client_id not in ongoing_conversations:
            ongoing_conversations[client_id] = {
                'manager_id': MANAGER_CHAT_ID,
                'client_id': client_id,
                'active': True
            }
            print(f"Added new entry in ongoing_conversations: {ongoing_conversations[client_id]}")

        manager_id = get_manager_for_client(client_id)
        if manager_id is None:
            print(f"No manager found for client {client_id}")
            return

        try:
            if message.text:
                bot.send_message(manager_id, f"💬 Сообщение от клиента {client_id}:\n{message.text}")
            elif message.photo:
                bot.send_photo(manager_id, message.photo[-1].file_id, caption=f"📷 Фото от клиента {client_id}")
            elif message.voice:
                bot.send_voice(manager_id, message.voice.file_id,
                               caption=f"🎙 Голосовое сообщение от клиента {client_id}")
            elif message.video:
                bot.send_video(manager_id, message.video.file_id, caption=f"🎥 Видео от клиента {client_id}")
            elif message.video_note:
                bot.send_video_note(manager_id, message.video_note.file_id)
                print(f"Forwarded video note from client {client_id} to manager {manager_id}")
            elif message.document:
                bot.send_document(manager_id, message.document.file_id, caption=f"📂 Документ от клиента {client_id}")

            print(f"Forwarded client message from {client_id} to manager {manager_id}")
        except Exception as e:
            print(f"❌ Ошибка при отправке сообщения от клиента {client_id} менеджеру: {e}")

    @bot.callback_query_handler(func=lambda call: call.data.startswith("client_"))
    def forward_message_to_selected_client(call: CallbackQuery):
        client_id = int(call.data.split("_")[1])
        manager_id = call.message.chat.id

        set_client_to_forward(manager_id, client_id)

        bot.send_message(manager_id, "Введите сообщение для клиента:")

    def send_photo_to_client(msg: Message):
        client_to_forward = ongoing_conversations[msg.chat.id].get('client_to_forward')

        if client_to_forward:
            bot.send_message(msg.chat.id, "✅ Фото отправлено клиенту.")
            del ongoing_conversations[msg.chat.id]['client_to_forward']