import telebot
from config import get_config
import handlers
from database.init_db import init_database
from set_logging import setup_logging
import logging

# logs
setup_logging()
logger = logging.getLogger(__name__)

# config
config = get_config()
token, admin_id, db_filename = config["token"], config["admin_id"], config["db_filename"]

# database
init_database(db_filename)

# bot

bot = telebot.TeleBot(token)
handlers.register_handlers(bot, db_filename)

logger.info("bot started")
bot.infinity_polling()