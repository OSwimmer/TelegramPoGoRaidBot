from telegram.ext import MessageHandler, Filters, CommandHandler, Updater, InlineQueryHandler, CallbackQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import logging
from conversation import get_add_raid_handler
import raid as r
from keyboard import get_keyboard


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


def button(bot, update):
    query = update.callback_query
    message = query.message
    user = query.from_user
    username = user.username
    print("message: " + str(message))
    data = format(query.data)
    new_message = message.text
    button_id, raid_id = extract_from_button(data)
    if button_id is "1":
        new_message = add_player_to_raid(username, message.text, raid_id)
    elif button_id is "2":
        new_message = add_person_to_player(username, message.text, raid_id)
    elif button_id is "3":
        new_message = remove_person_from_player(username, message.text, raid_id)
    elif button_id is "4":
        new_message = remove_player_from_raid(username, message.text, raid_id)
    bot.edit_message_text(chat_id=r.group_chat_id, message_id=message.message_id, text=new_message, reply_markup=get_keyboard(raid_id))


def extract_from_button(data):
    splitted = data.split(",")
    return splitted[0], int(splitted[1])


def add_person_to_player(user, message, raid_id):
    r.add_person_to_player(user, raid_id)
    return r.get_full_raid_message(raid_id)


def add_player_to_raid(user, message, raid_id):
    r.add_player_to_raid(user, raid_id)
    return r.get_full_raid_message(raid_id)
    # return message + "\n  " + user


def remove_person_from_player(user, message, raid_id):
    r.remove_person_from_player(user, raid_id)
    return r.get_full_raid_message(raid_id)


def remove_player_from_raid(user, message, raid_id):
    r.remove_player_from_raid(user, raid_id)
    return r.get_full_raid_message(raid_id)


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

    callback_handler = CallbackQueryHandler(button)
    dispatcher.add_handler(callback_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)


def main():
    updater = Updater(token='430567701:AAH4_O4uu19JFTXhf2Sw-hmTgoi7tWSFWkk')
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    add_handlers(dispatcher)
    updater.start_polling()
    print("Bot started!")


if __name__ == '__main__':
    main()
