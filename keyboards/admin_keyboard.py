from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_main_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="users", callback_data="admin_users"),
        InlineKeyboardButton(text="back", callback_data="main_menu"),
    )
    return markup