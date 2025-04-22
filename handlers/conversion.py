from telebot.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import get_conversion_menu, get_inline_menu
from currency import convert_eur_to_rub, convert_usd_to_rub

def show_conversion_buttons_simulated(bot, message):
    bot.send_message(message.chat.id, "Выберите валюту для новой конвертации:", reply_markup=get_conversion_menu())

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
        bot.register_next_step_handler(call.message, process_eur_conversion)

    @bot.callback_query_handler(func=lambda call: call.data == "convert_usd_rub")
    def ask_usd_to_rub(call: CallbackQuery):
        bot.send_message(call.message.chat.id, "Введите сумму в долларах ($) - указывайте число без знака и пробелов:")
        bot.register_next_step_handler(call.message, process_usd_conversion)

    def process_eur_conversion(message: Message):
        try:
            amount = float(message.text)
            converted_amount, _ = convert_eur_to_rub(amount)
            final_amount = round(converted_amount * 1.37 / 10) * 10

            conversion_menu = InlineKeyboardMarkup()
            conversion_menu.add(InlineKeyboardButton("📞 Связаться с менеджером", callback_data="contact_manager"))
            conversion_menu.add(
                InlineKeyboardButton("€ → ₽", callback_data="convert_eur_rub"),
                InlineKeyboardButton("$ → ₽", callback_data="convert_usd_rub")
            )
            conversion_menu.add(InlineKeyboardButton("⬅ Назад в меню", callback_data="back_to_main"))

            bot.send_message(
                message.chat.id,
                f"💰 {amount} € = {final_amount} ₽ — сумма указана с учётом стоимости услуг.\nОбратите внимание: расчёт предварительный. Курс валют может меняться, поэтому за точной стоимостью рекомендуем обратиться к менеджеру.",
                reply_markup=conversion_menu
            )
        except ValueError:
            bot.send_message(message.chat.id, "❌ Ошибка! Введите корректное число.\nСначала выберите нужный вариант валюты из меню, затем введите сумму.")

    def process_usd_conversion(message: Message):
        try:
            amount = float(message.text)
            converted_amount, _ = convert_usd_to_rub(amount)
            final_amount = round(converted_amount * 1.47 / 10) * 10

            conversion_menu = InlineKeyboardMarkup()
            conversion_menu.add(InlineKeyboardButton("📞 Связаться с менеджером", callback_data="contact_manager"))
            conversion_menu.add(
                InlineKeyboardButton("€ → ₽", callback_data="convert_eur_rub"),
                InlineKeyboardButton("$ → ₽", callback_data="convert_usd_rub")
            )
            conversion_menu.add(InlineKeyboardButton("⬅ Назад в меню", callback_data="back_to_main"))

            bot.send_message(
                message.chat.id,
                f"💰 {amount} $ = {final_amount} ₽  — сумма указана с учётом стоимости услуг.\nОбратите внимание: расчёт предварительный. Курс валют может меняться, поэтому за точной стоимостью рекомендуем обратиться к менеджеру.",
                reply_markup=conversion_menu
            )
        except ValueError:
            bot.send_message(message.chat.id, "❌ Ошибка! Введите корректное число.\nСначала выберите нужный вариант валюты из меню, затем введите сумму.")