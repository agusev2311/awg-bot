from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_main_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="👥 Users", callback_data="admin_users"),
        InlineKeyboardButton(text="🧩 All configs", callback_data="admin_configs"),
        InlineKeyboardButton(text="⬅ Back", callback_data="main_menu"),
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

    markup.add(InlineKeyboardButton(text="⬅ Back", callback_data="admin_panel"))
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
    markup.add(InlineKeyboardButton(text="🔢 Change config limit", callback_data=f"admin_user_limit:{user_id}:{page}"))
    markup.add(InlineKeyboardButton(text="⬅ Back", callback_data=f"admin_users:{page}"))
    return markup

def user_configs_keyboard(configs: list[dict], page: int, total_configs: int, per_page: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    markup.add(InlineKeyboardButton(text="➕ New config", callback_data="user_configs_new"))

    for config in configs:
        title = config["name"] or f"config #{config['id']}"
        status_icon = "🟢" if config["status"] == "active" else "⏸"
        markup.add(InlineKeyboardButton(text=f"{status_icon} {title}", callback_data=f"user_config:{config['id']}:{page}"))

    total_pages = max((total_configs + per_page - 1) // per_page, 1)
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text="<", callback_data=f"user_configs:{page - 1}"))
    nav_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="user_configs_noop"))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton(text=">", callback_data=f"user_configs:{page + 1}"))
    markup.row(*nav_buttons)

    markup.add(InlineKeyboardButton(text="⬅ Back", callback_data="main_menu"))
    return markup

def user_config_keyboard(config_id: int, page: int, status: str, admin_page: int | None = None) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    toggle_title = "⏸ Pause" if status == "active" else "▶ Resume"
    toggle_status = "paused" if status == "active" else "active"

    markup.row(
        InlineKeyboardButton(text="✏️ Rename", callback_data=f"config_rename:{config_id}:{page}:{admin_page or 0}"),
        InlineKeyboardButton(text=toggle_title, callback_data=f"config_status:{config_id}:{page}:{admin_page or 0}:{toggle_status}"),
    )
    markup.add(InlineKeyboardButton(text="🗑 Delete", callback_data=f"config_delete:{config_id}:{page}:{admin_page or 0}"))

    if admin_page is None:
        markup.add(InlineKeyboardButton(text="⬇ Download", callback_data=f"user_config_download:{config_id}:{page}"))
        markup.add(InlineKeyboardButton(text="⬅ Back", callback_data=f"user_configs:{page}"))
    else:
        markup.add(InlineKeyboardButton(text="⬇ Download", callback_data=f"admin_config_download:{config_id}:{admin_page}"))
        markup.add(InlineKeyboardButton(text="⬅ Back", callback_data=f"admin_configs:{admin_page}"))

    return markup

def admin_configs_keyboard(configs: list[dict], page: int, total_configs: int, per_page: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    for config in configs:
        title = config["name"] or f"config #{config['id']}"
        status_icon = "🟢" if config["status"] == "active" else "⏸"
        markup.add(InlineKeyboardButton(text=f"{status_icon} #{config['id']} {title}", callback_data=f"admin_config:{config['id']}:{page}"))

    total_pages = max((total_configs + per_page - 1) // per_page, 1)
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text="<", callback_data=f"admin_configs:{page - 1}"))
    nav_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="admin_configs_noop"))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton(text=">", callback_data=f"admin_configs:{page + 1}"))
    markup.row(*nav_buttons)

    markup.add(InlineKeyboardButton(text="⬅ Back", callback_data="admin_panel"))
    return markup
