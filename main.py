import telebot
from config import get_config
import handlers
from database.init_db import init_database

# config
config = get_config()
token, admin_id, db_filename = config["token"], config["admin_id"], config["db_filename"]

# database
init_database(db_filename)

# bot

bot = telebot.TeleBot(token)
handlers.register_handlers(bot)

bot.infinity_polling()