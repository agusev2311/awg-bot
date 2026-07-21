from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_main_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="users", callback_data="admin_users"),
        InlineKeyboardButton(text="back", callback_data="main_menu"),
    )
    return markup

def admin_users_keyboard(users: list[dict], page: int, total_users: int, per_page: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    for user in users:
        markup.add(
            InlineKeyboardButton(
                text=f"{user['id']} [{user['status']}]",
                callback_data=f"admin_user:{user['id']}:{page}",
            )
        )

    total_pages = max((total_users + per_page - 1) // per_page, 1)
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text="<", callback_data=f"admin_users:{page - 1}"))
    nav_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="admin_users_noop"))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton(text=">", callback_data=f"admin_users:{page + 1}"))
    markup.row(*nav_buttons)

    markup.add(InlineKeyboardButton(text="back", callback_data="admin_panel"))
    return markup

def admin_user_keyboard(user_id: int, page: int, current_status: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    statuses = ["ok", "not_approved", "banned"]

    buttons = []
    for status in statuses:
        title = f"{status} {'*' if status == current_status else ''}".strip()
        buttons.append(
            InlineKeyboardButton(
                text=title,
                callback_data=f"admin_user_status:{user_id}:{page}:{status}",
            )
        )
    markup.row(*buttons)
    markup.add(InlineKeyboardButton(text="change config limit", callback_data=f"admin_user_limit:{user_id}:{page}"))
    markup.add(InlineKeyboardButton(text="back", callback_data=f"admin_users:{page}"))
    return markup

def user_configs_keyboard(configs: list[dict], page: int, total_configs: int, per_page: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    markup.add(InlineKeyboardButton(text="new config", callback_data="user_configs_new"))

    for config in configs:
        title = config["name"] or f"config #{config['id']}"
        markup.add(InlineKeyboardButton(text=title, callback_data=f"user_config:{config['id']}:{page}"))

    total_pages = max((total_configs + per_page - 1) // per_page, 1)
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text="<", callback_data=f"user_configs:{page - 1}"))
    nav_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="user_configs_noop"))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton(text=">", callback_data=f"user_configs:{page + 1}"))
    markup.row(*nav_buttons)

    markup.add(InlineKeyboardButton(text="back", callback_data="main_menu"))
    return markup
