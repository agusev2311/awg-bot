from keyboards.start_keyboard import start_keyboard
from keyboards.admin_keyboard import admin_main_keyboard, admin_users_keyboard, admin_user_keyboard
from database import users
import config

USERS_PER_PAGE = 10

def _get_user_title(bot, user_id: int) -> str:
    try:
        chat = bot.get_chat(user_id)
    except Exception:
        return str(user_id)

    full_name = " ".join(part for part in [chat.first_name, chat.last_name] if part)
    if getattr(chat, "username", None):
        username = f"@{chat.username}"
        return f"{full_name} ({username})" if full_name else username
    return full_name or str(user_id)

def _render_users_page(bot, call, db_filename, page: int):
    users_page, total_users = users.get_users_page(db_filename, page, USERS_PER_PAGE)
    total_pages = max((total_users + USERS_PER_PAGE - 1) // USERS_PER_PAGE, 1)
    page = min(max(page, 1), total_pages)

    if not users_page and page > 1:
        users_page, total_users = users.get_users_page(db_filename, total_pages, USERS_PER_PAGE)
        page = total_pages

    text_lines = [f"Users page {page}/{total_pages}"]
    if users_page:
        text_lines.append("")
        for user in users_page:
            user_title = _get_user_title(bot, user["id"])
            text_lines.append(f"{user['id']} | {user_title} | {user['status']} | configs: {user['configs_count']}")
    else:
        text_lines.append("")
        text_lines.append("No users")

    bot.edit_message_text(
        text="\n".join(text_lines),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=admin_users_keyboard(users_page, page, total_users, USERS_PER_PAGE),
    )

def _render_user_card(bot, call, db_filename, user_id: int, page: int):
    user = users.get_user_by_id(db_filename, user_id)
    if not user:
        bot.answer_callback_query(call.id, "User not found")
        _render_users_page(bot, call, db_filename, page)
        return

    user_title = _get_user_title(bot, user_id)

    bot.edit_message_text(
        text=(
            f"User {user['id']}\n\n"
            f"Name: {user_title}\n"
            f"Status: {user['status']}\n"
            f"Configs: {user['configs_count']}"
        ),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=admin_user_keyboard(user_id, page, user["status"]),
    )

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

    @bot.callback_query_handler(func=lambda call: call.data == "admin_users")
    def handle_admin_users(call):
        bot.answer_callback_query(call.id)
        _render_users_page(bot, call, db_filename, 1)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("admin_users:"))
    def handle_admin_users_page(call):
        bot.answer_callback_query(call.id)
        _, page = call.data.split(":")
        _render_users_page(bot, call, db_filename, int(page))

    @bot.callback_query_handler(func=lambda call: call.data == "admin_users_noop")
    def handle_admin_users_noop(call):
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("admin_user:"))
    def handle_admin_user(call):
        bot.answer_callback_query(call.id)
        _, user_id, page = call.data.split(":")
        _render_user_card(bot, call, db_filename, int(user_id), int(page))

    @bot.callback_query_handler(func=lambda call: call.data.startswith("admin_user_status:"))
    def handle_admin_user_status(call):
        _, user_id, page, status = call.data.split(":")
        users.set_status(db_filename, int(user_id), status)
        bot.answer_callback_query(call.id, f"Status changed to {status}")
        _render_user_card(bot, call, db_filename, int(user_id), int(page))
