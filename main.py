from telegram.ext import MessageHandler, Filters, CommandHandler, Updater, InlineQueryHandler, CallbackQueryHandler
from telegram import ParseMode, Location
from conversation import get_add_raid_handler
from keyboard import get_keyboard
import raid as r
import static_data as s

import logging, requests, time, threading, configparser


def get_chat_id(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="chat id is " + str(update.message.chat_id))


def button(bot, update):
    query = update.callback_query
    message = query.message
    user = query.from_user
    username = user.username
    if username is None:
        username = user.first_name
    data = format(query.data)
    new_message = message.text
    button_id, raid_id = extract_from_button(data)
    if button_id is s.ADD_PLAYER_BUTTON_SLOT1:
        new_message = add_player_to_raid(username, message.text, raid_id, 0)
    elif button_id is s.ADD_PLAYER_BUTTON_SLOT2:
        new_message = add_player_to_raid(username, message.text, raid_id, 1)
    elif button_id is s.ADD_PERSON_BUTTON:
        new_message = add_person_to_player(username, message.text, raid_id)
    elif button_id is s.REMOVE_PERSON_BUTTON:
        new_message = remove_person_from_player(username, message.text, raid_id)
    elif button_id is s.PLAYER_ARRIVED_BUTTON:
        new_message = player_has_arrived(username, message.text, raid_id)
    elif button_id is s.REMOVE_PLAYER_BUTTON:
        new_message = remove_player_from_raid(username, message.text, raid_id)
    bot.edit_message_text(chat_id=s.group_chat_id, message_id=message.message_id, text=new_message, reply_markup=get_keyboard(raid_id), parse_mode=ParseMode.MARKDOWN)


def extract_from_button(data):
    splitted = data.split(",")
    return splitted[0], int(splitted[1])


def player_has_arrived(user, message, raid_id):
    r.player_has_arrived(user, raid_id)
    return r.get_full_raid_message(raid_id)


def add_person_to_player(user, message, raid_id):
    r.add_person_to_player(user, raid_id)
    return r.get_full_raid_message(raid_id)


def add_player_to_raid(user, message, raid_id, timeslot):
    r.add_player_to_raid(user, raid_id, timeslot)
    return r.get_full_raid_message(raid_id)


def remove_person_from_player(user, message, raid_id):
    r.remove_person_from_player(user, raid_id)
    return r.get_full_raid_message(raid_id)


def remove_player_from_raid(user, message, raid_id):
    r.remove_player_from_raid(user, raid_id)
    return r.get_full_raid_message(raid_id)


def add_test_raid(bot, update):
    r.set_boss(r.global_raid_id, "TestBoss")
    r.set_gym(r.global_raid_id, "TestGym")
    location = Location(4.456874, 50.878761)
    r.set_location(r.global_raid_id, location)
    r.set_moveset(r.global_raid_id, ["TestQuick", "TestCharged"])
    r.set_opentime(r.global_raid_id, "12:00")
    r.set_timeslots(r.global_raid_id, ["12:05", "12:35"])

    reply_markup = get_keyboard(r.global_raid_id)
    bot.send_location(chat_id=update.message.chat_id, location=r.get_location(r.global_raid_id))
    bot.send_message(chat_id=update.message.chat_id, text=r.get_raid_info_as_string(r.global_raid_id), reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    r.global_raid_id += 1


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


def silence(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Ssshh %s, you are beautiful when you don't talk" % update.message.from_user.username)


def add_handlers(dispatcher):
    add_raid_handler = get_add_raid_handler()
    dispatcher.add_handler(add_raid_handler)
    chat_id_handler = CommandHandler('chatid', get_chat_id)
    dispatcher.add_handler(chat_id_handler)

    add_test_raid_handler = CommandHandler('testRaid', add_test_raid)
    dispatcher.add_handler(add_test_raid_handler)

    # dispatcher.add_handler(rb.get_raid_bot_handler())

    callback_handler = CallbackQueryHandler(button)
    dispatcher.add_handler(callback_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    lulz_handler = MessageHandler(Filters.text, silence)
    dispatcher.add_handler(lulz_handler)


def pull_api():
    print(time.ctime())
    threading.Timer(60, pull_api).start()


def main():
    config = configparser.ConfigParser()
    config.read("properties.ini")
    updater = Updater(token=config["TelegramSettings"]["token"])
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    add_handlers(dispatcher)
    updater.start_polling(timeout=20)
    # pull_api()
    print("Bot started!")


if __name__ == '__main__':
    main()
