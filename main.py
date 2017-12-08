from telegram.ext import MessageHandler, Filters, CommandHandler, Updater, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup
import logging
from conversation import get_add_raid_handler


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


def moo(message):
    cow = (
        ".        (__) \n"
        "         (oo) \n"
        "   /------\/  \n"
        "  / |    ||   \n"
        " *  /\---/\   \n"
        "    ~~   ~~   \n"
        " ")
    return cow + message


def inline_iets(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query + "doet dit iets?",
            title="Hetzelfde",
            input_message_content=InputTextMessageContent(query.upper() + " ik zeg altijd hetzelfde :v")
        )
    )
    results.append(
        InlineQueryResultArticle(
            id=query + "moo",
            title="MOO",
            input_message_content=InputTextMessageContent(moo(query))
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)


def get_chat_id(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="chat id is " + str(update.message.chat_id))


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


def add_handlers(dispatcher):
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    caps_handler = CommandHandler('caps', caps, pass_args=True)
    dispatcher.add_handler(caps_handler)
    inline_hetzelfde = InlineQueryHandler(inline_iets)
    dispatcher.add_handler(inline_hetzelfde)
    add_raid_handler = get_add_raid_handler()
    dispatcher.add_handler(add_raid_handler)
    chat_id_handler = CommandHandler('chatid', get_chat_id)
    dispatcher.add_handler(chat_id_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)


def main():
    updater = Updater(token='430567701:AAH4_O4uu19JFTXhf2Sw-hmTgoi7tWSFWkk')
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    add_handlers(dispatcher)
    updater.start_polling()


if __name__ == '__main__':
    main()
