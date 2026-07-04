import telebot
from database import users

def register_handlers(bot, db_filename):
    @bot.message_handler(commands=["start"])
    def send_welcome(message):
        users.create_user_if_not_exist(db_filename, int(message.from_user.id))
        bot.reply_to(message, "Hi!")
        
    @bot.message_handler(commands=["ping"])
    def ping(message):
        bot.reply_to(message, "Pong")