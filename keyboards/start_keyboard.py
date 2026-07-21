from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_keyboard(is_admin: bool) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="📦 My configs", callback_data="user_configs"),
    )
    if is_admin:
        markup.add(InlineKeyboardButton(text="🛠 Admin panel", callback_data="admin_panel", icon_custom_emoji_id="5411166821636145837"),)
    return markup
