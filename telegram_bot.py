import telebot
from config import TOKEN, MANAGER_CHAT_ID
from handlers.handlers import register_handlers

class TelegramBot:
    def __init__(self):
        self.bot = telebot.TeleBot(TOKEN)
        self.manager_id = MANAGER_CHAT_ID
        self.clients = {}

        register_handlers(self)
