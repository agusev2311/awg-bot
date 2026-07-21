import telebot
from database import users
import work_with_awg
import io
from work_with_awg import generate_client_config
from keyboards.start_keyboard import start_keyboard
import config

def _is_banned(db_filename: str, user_id: int) -> bool:
    return users.get_status(db_filename, user_id) == "banned"

def register_handlers(bot, db_filename):
    @bot.message_handler(commands=["start"])
    def send_welcome(message):
        user_id = int(message.from_user.id)
        users.create_user_if_not_exist(db_filename, user_id)
        user_status = users.get_status(db_filename, user_id)

        if user_status == "ok":
            bot.send_message(message.chat.id, "Welcome!",
                             reply_markup=start_keyboard(user_id == int(config.get_config()["admin_id"])))
        elif user_status == "banned":
            bot.reply_to(message, "Your account has been banned")
        else:
            bot.reply_to(message, "Your account is not approved yet. Please contact administrator or just wait")

    @bot.message_handler(func=lambda message: _is_banned(db_filename, int(message.from_user.id)))
    def handle_banned_message(message):
        bot.reply_to(message, "Your account has been banned")

    # @bot.message_handler(commands=["new_config"])
    # def new_config(message):
    #     user_id = message.from_user.id
    #     new_conf_id = work_with_awg.new_user_config(user_id)
    #     conf = generate_client_config.generate(new_conf_id)

    #     file_buffer = io.BytesIO(conf.encode("utf-8"))
    #     file_buffer.name = f"awg_{new_conf_id}.conf"

    #     bot.send_document(chat_id=message.chat.id, document=file_buffer,)
