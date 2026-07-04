import telebot
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("AWG_TG_TOKEN")
admin_id = os.getenv("AWG_TG_ADMIN_ID")
bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Hi!")
    
@bot.message_handler(commands=["ping"])
def ping(message):
    bot.reply_to(message, "Pong")

bot.infinity_polling()