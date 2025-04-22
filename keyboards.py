from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TELEGRAM_CATALOG_LINK, TELEGRAM_REVIEWS

def get_inline_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📞 Связаться с менеджером", callback_data="contact_manager"))
    markup.add(InlineKeyboardButton("💱 Конвертация валют", callback_data="conversion"))
    markup.add(InlineKeyboardButton("🛍 Каталог", url=TELEGRAM_CATALOG_LINK))
    markup.add(InlineKeyboardButton("📦 Доставка", callback_data="delivery"))
    markup.add(InlineKeyboardButton("🗣️ Отзывы", url=TELEGRAM_REVIEWS))
    return markup

def get_conversion_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("€ → ₽", callback_data="convert_eur_rub"))
    markup.add(InlineKeyboardButton("$ → ₽", callback_data="convert_usd_rub"))
    markup.add(InlineKeyboardButton("⬅ Назад", callback_data="back_to_main"))
    return markup