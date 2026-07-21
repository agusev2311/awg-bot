from keyboards.start_keyboard import start_keyboard
from keyboards.admin_keyboard import admin_main_keyboard, admin_users_keyboard, admin_user_keyboard, user_configs_keyboard
from database import users, configs
import config
import io
import re
import work_with_awg
from work_with_awg import generate_client_config

USERS_PER_PAGE = 10
CONFIGS_PER_PAGE = 10

def _build_config_filename(name: str, fallback: str) -> str:
    safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", name).strip("._")
    return safe_name or fallback

def _is_banned(db_filename: str, user_id: int) -> bool:
    return users.get_status(db_filename, user_id) == "banned"

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
    effective_limit = users.get_effective_configs_limit(db_filename, user_id)
    limit_line = user["configs_limit"] if user["configs_limit"] is not None else f"default ({effective_limit})"

    bot.edit_message_text(
        text=(
            f"User {user['id']}\n\n"
            f"Name: {user_title}\n"
            f"Status: {user['status']}\n"
            f"Configs: {user['configs_count']}\n"
            f"Config limit: {limit_line}"
        ),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=admin_user_keyboard(user_id, page, user["status"]),
    )

def _render_user_configs_page(bot, call, db_filename, user_id: int, page: int):
    configs_page, total_configs = configs.get_user_configs_page(db_filename, user_id, page, CONFIGS_PER_PAGE)
    total_pages = max((total_configs + CONFIGS_PER_PAGE - 1) // CONFIGS_PER_PAGE, 1)
    page = min(max(page, 1), total_pages)

    if not configs_page and page > 1:
        configs_page, total_configs = configs.get_user_configs_page(db_filename, user_id, total_pages, CONFIGS_PER_PAGE)
        page = total_pages

    limit = users.get_effective_configs_limit(db_filename, user_id)
    text_lines = [f"My configs {page}/{total_pages}", f"Used: {total_configs}/{limit}"]
    if configs_page:
        text_lines.append("")
        for config_item in configs_page:
            title = config_item["name"] or f"config #{config_item['id']}"
            text_lines.append(f"{config_item['id']} | {title}")
    else:
        text_lines.append("")
        text_lines.append("No configs")

    bot.edit_message_text(
        text="\n".join(text_lines),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=user_configs_keyboard(configs_page, page, total_configs, CONFIGS_PER_PAGE),
    )

def register_handlers(bot, db_filename):
    @bot.callback_query_handler(func=lambda call: _is_banned(db_filename, int(call.from_user.id)))
    def handle_banned_callback(call):
        bot.answer_callback_query(call.id, "Your account has been banned")

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

    @bot.callback_query_handler(func=lambda call: call.data.startswith("admin_user_limit:"))
    def handle_admin_user_limit(call):
        _, user_id, page = call.data.split(":")
        bot.answer_callback_query(call.id)
        sent = bot.send_message(call.message.chat.id, "Send new config limit number for this user. Send 0 to reset to default.")

        def process_limit(message):
            if int(message.from_user.id) != int(config.get_config()["admin_id"]):
                return
            try:
                limit = int(message.text.strip())
                if limit < 0:
                    raise ValueError
            except (TypeError, ValueError):
                bot.reply_to(message, "Limit must be a non-negative integer")
                return

            users.set_configs_limit(db_filename, int(user_id), None if limit == 0 else limit)
            bot.reply_to(message, "User config limit updated")

        bot.register_next_step_handler(sent, process_limit)

    @bot.callback_query_handler(func=lambda call: call.data == "user_configs")
    def handle_user_configs(call):
        bot.answer_callback_query(call.id)
        _render_user_configs_page(bot, call, db_filename, int(call.from_user.id), 1)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("user_configs:"))
    def handle_user_configs_page(call):
        bot.answer_callback_query(call.id)
        _, page = call.data.split(":")
        _render_user_configs_page(bot, call, db_filename, int(call.from_user.id), int(page))

    @bot.callback_query_handler(func=lambda call: call.data == "user_configs_noop")
    def handle_user_configs_noop(call):
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda call: call.data == "user_configs_new")
    def handle_user_configs_new(call):
        bot.answer_callback_query(call.id)
        user_id = int(call.from_user.id)
        current_count = configs.count_user_configs(db_filename, user_id)
        limit = users.get_effective_configs_limit(db_filename, user_id)
        if current_count >= limit:
            bot.send_message(call.message.chat.id, f"Config limit reached: {current_count}/{limit}")
            return

        sent = bot.send_message(call.message.chat.id, "Send config name")

        def process_config_name(message):
            if int(message.from_user.id) != user_id:
                return
            config_name = (message.text or "").strip()
            if not config_name:
                bot.reply_to(message, "Config name cannot be empty")
                return

            current_total = configs.count_user_configs(db_filename, user_id)
            current_limit = users.get_effective_configs_limit(db_filename, user_id)
            if current_total >= current_limit:
                bot.reply_to(message, f"Config limit reached: {current_total}/{current_limit}")
                return

            config_id = work_with_awg.new_user_config(user_id, config_name)
            config_text = generate_client_config.generate(config_id)
            file_buffer = io.BytesIO(config_text.encode("utf-8"))
            file_buffer.name = f"{_build_config_filename(config_name, f'config_{config_id}')}.conf"
            bot.send_document(chat_id=message.chat.id, document=file_buffer)
            bot.send_message(message.chat.id, "Config created")

        bot.register_next_step_handler(sent, process_config_name)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("user_config:"))
    def handle_user_config(call):
        bot.answer_callback_query(call.id)
        _, config_id, page = call.data.split(":")
        user_config = configs.get_user_config_by_id(db_filename, int(call.from_user.id), int(config_id))
        if not user_config:
            bot.answer_callback_query(call.id, "Config not found")
            _render_user_configs_page(bot, call, db_filename, int(call.from_user.id), int(page))
            return

        config_text = generate_client_config.generate(int(config_id))
        file_buffer = io.BytesIO(config_text.encode("utf-8"))
        config_name = user_config["name"] or f"config_{config_id}"
        file_buffer.name = f"{_build_config_filename(config_name, f'config_{config_id}')}.conf"
        bot.send_document(chat_id=call.message.chat.id, document=file_buffer)
