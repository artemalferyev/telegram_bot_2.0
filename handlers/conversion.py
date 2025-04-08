from telebot.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import get_conversion_menu, get_inline_menu
from currency import convert_eur_to_rub, convert_usd_to_rub

def register_conversion_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "conversion")
    def show_conversion_buttons(call: CallbackQuery):
        print("✅ Кнопка 'conversion' нажата")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=get_conversion_menu())

    @bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
    def back_to_main(call: CallbackQuery):
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=get_inline_menu())

    @bot.callback_query_handler(func=lambda call: call.data == "convert_eur_rub")
    def ask_eur_to_rub(call: CallbackQuery):
        bot.send_message(call.message.chat.id, "Введите сумму в евро (€) - указывайте число без знака и пробелов:")
        bot.register_next_step_handler(call.message, process_conversion, convert_eur_to_rub, "€", "₽")

    @bot.callback_query_handler(func=lambda call: call.data == "convert_usd_rub")
    def ask_usd_to_rub(call: CallbackQuery):
        bot.send_message(call.message.chat.id, "Введите сумму в долларах ($) - указывайте число без знака и пробелов:")
        bot.register_next_step_handler(call.message, process_conversion, convert_usd_to_rub, "$", "₽")

    def process_conversion(message: Message, conversion_func, source_currency, target_currency):
        try:
            amount = float(message.text)
            converted_amount, _ = conversion_func(amount)

            final_amount = round(converted_amount * 1.42, -1)

            conversion_menu = InlineKeyboardMarkup()
            conversion_menu.add(InlineKeyboardButton("📞 Связаться с менеджером", callback_data="contact_manager"))
            conversion_menu.add(InlineKeyboardButton("⬅ Назад", callback_data="conversion"))

            bot.send_message(
                message.chat.id,
                f"💰 {amount} {source_currency} = {final_amount} {target_currency} (с учетом стоимости доставки и услуг)",
                reply_markup=conversion_menu
            )
        except ValueError:
            bot.send_message(message.chat.id, "❌ Ошибка! Введите корректное число.")