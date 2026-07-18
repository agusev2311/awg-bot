from . import basic, callbacks

def register_handlers(bot, db_filename):
    basic.register_handlers(bot, db_filename)
    callbacks.register_handlers(bot, db_filename)