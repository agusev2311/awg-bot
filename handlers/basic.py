import telebot

def register_handlers(bot):
    @bot.message_handler(commands=["start"])
    def send_welcome(message):
        bot.reply_to(message, "Hi!")
        
    @bot.message_handler(commands=["ping"])
    def ping(message):
        bot.reply_to(message, "Pong")