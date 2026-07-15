import telebot
from database import users
import work_with_awg
import io
from work_with_awg import generate_client_config

def register_handlers(bot, db_filename):
    @bot.message_handler(commands=["start"])
    def send_welcome(message):
        users.create_user_if_not_exist(db_filename, int(message.from_user.id))
        bot.reply_to(message, "Hi!")
        
    @bot.message_handler(commands=["ping"])
    def ping(message):
        bot.reply_to(message, "Pong")

    @bot.message_handler(commands=["new_config"])
    def new_config(message):
        user_id = message.from_user.id
        new_conf_id = work_with_awg.new_user_config(user_id)
        conf = generate_client_config.generate(new_conf_id)

        file_buffer = io.BytesIO(conf.encode("utf-8"))
        file_buffer.name = f"awg_{new_conf_id}.conf"

        bot.send_document(chat_id=message.chat.id, document=file_buffer,)