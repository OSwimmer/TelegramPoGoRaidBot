from telegram.ext import MessageHandler, Filters

import raid as r


def parse_message(bot, update):
    print(str(update))
    return


def get_raid_bot_handler():
    raid_bot_handler = MessageHandler(callback=parse_message, filters=Filters.chat(chat_id=r.group_chat_id))
    return raid_bot_handler
