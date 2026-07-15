import telebot
from config import get_config
import handlers
from database.init_db import init_database
from set_logging import setup_logging
import logging
from work_with_awg import check

# logs
setup_logging()
logger = logging.getLogger(__name__)
logger.info("logger init")

# config
config = get_config()
token, admin_id, db_filename, awg_dir, awg_subnet, awg_subnet_v6, awg_endpoint, awg_public = config["token"], config["admin_id"], config["db_filename"], config["awg_dir"], config["awg_subnet"], config["awg_subnet_v6"], config["awg_endpoint"], config["awg_public"]

# database
init_database(db_filename)

# check amnezia
if not check.check_amnezia():
    exit(1)

# bot
bot = telebot.TeleBot(token)
handlers.register_handlers(bot, db_filename)

logger.info("bot started")
bot.infinity_polling()