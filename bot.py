from telebot import TeleBot
from telebot.types import BotCommand, BotCommandScopeChat
from config import MANAGER_CHAT_ID

from config import TOKEN
from handlers.handlers import register_handlers

bot = TeleBot(TOKEN)

def set_manager_commands():
    commands = [
        BotCommand("start", "Главное меню"),
        BotCommand("clients", "Показать активных клиентов")
    ]
    scope = BotCommandScopeChat(chat_id=MANAGER_CHAT_ID)
    bot.set_my_commands(commands, scope=scope)

register_handlers(bot)
set_manager_commands()
bot.polling(timeout=60)