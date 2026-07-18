from keyboards.start_keyboard import start_keyboard
from keyboards.admin_keyboard import admin_main_keyboard
import config

def register_handlers(bot, db_filename):
    @bot.callback_query_handler(func=lambda call: call.data == "ping")
    def handle_get_config(call):
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "pong")

    @bot.callback_query_handler(func=lambda call: call.data == "admin_panel")
    def handle_get_config(call):
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            text="welcome, admin :3",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=admin_main_keyboard()
        )

    @bot.callback_query_handler(func=lambda call: call.data == "main_menu")
    def handle_main_menu(call):
        bot.answer_callback_query(call.id)
        is_admin = int(call.from_user.id) == int(config.get_config()["admin_id"])
        bot.edit_message_text(
            text="Welcome!",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=start_keyboard(is_admin)
        )