import telebot
from config import get_config
import handlers

config = get_config()
token, admin_id = config["token"], config["admin_id"]

bot = telebot.TeleBot(token)
handlers.register_handlers(bot)

bot.infinity_polling()