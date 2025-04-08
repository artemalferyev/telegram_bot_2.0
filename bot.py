from telebot import TeleBot

from config import TOKEN
from handlers.handlers import register_handlers

bot = TeleBot(TOKEN)
register_handlers(bot)
bot.polling(timeout=50)