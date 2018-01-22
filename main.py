from telegram.ext import MessageHandler, Filters, CommandHandler, Updater, CallbackQueryHandler
from telegram import ParseMode, Location
from conversation import get_add_raid_handler
from keyboard import get_keyboard
import raid as r
import static_data as s

import logging, requests, time, threading, random
import datetime as dt


current_day = dt.datetime.now().date()


def get_chat_id(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="chat id is " + str(update.message.chat_id))


def get_user_id(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="user id is " + str(update.message.from_user.id))


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
    if not r.is_raid_ongoing(raid_id):
        print("raid ended")
        bot.edit_message_reply_markup(chat_id=s.group_chat_id, message_id=message.message_id, text=message.text, reply_markup=None, parse_mode=ParseMode.MARKDOWN)
        r.remove_raid(raid_id)
        return
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
    r.save_raids_to_file()
    bot.edit_message_text(chat_id=s.group_chat_id, message_id=message.message_id, text=new_message, reply_markup=get_keyboard(raid_id), parse_mode=ParseMode.MARKDOWN)


def extract_from_button(data):
    splitted = data.split(",")
    return splitted[0], splitted[1]


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
    r.init_raid()
    r.set_boss(r.global_raid_id, str(random.randint(1, 387)))
    r.set_gym(r.global_raid_id, "TestGym")
    location = Location(4.456874, 50.878761)
    r.set_location_with_object(r.global_raid_id, location)
    r.set_moveset(r.global_raid_id, [str(random.randint(1, 281)), str(random.randint(1, 281))])
    now_obj = dt.datetime.now()
    now = now_obj.strftime('%H:%M:%S')
    r.set_opentime(r.global_raid_id, now)
    slot1, slot2 = r.calculate_timeslots(now_obj)
    r.set_timeslots(r.global_raid_id, [slot1, slot2])

    reply_markup = get_keyboard(r.global_raid_id)
    bot.send_location(chat_id=update.message.chat_id, location=r.get_location_as_object(r.global_raid_id))
    bot.send_message(chat_id=update.message.chat_id, text=r.get_raid_info_as_string(r.global_raid_id), reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    r.increment_global_raid_id()


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


def silence(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Ssshh %s, you are beautiful when you don't talk" % update.message.from_user.username)


def load_state_from_file(bot, update):
    if r.load_raids_from_file():
        bot.send_message(chat_id=update.message.chat_id, text="Raids zijn succesvol ingeladen!")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Er was een probleem bij het inladen van de raids, check of de config correct is.")


def add_handlers(dispatcher):
    add_raid_handler = get_add_raid_handler()
    dispatcher.add_handler(add_raid_handler)
    chat_id_handler = CommandHandler('chatid', get_chat_id)
    dispatcher.add_handler(chat_id_handler)
    user_id_handler = CommandHandler('userid', get_user_id)
    dispatcher.add_handler(user_id_handler)

    add_test_raid_handler = CommandHandler('testRaid', add_test_raid, filters=Filters.user(s.get_admins()))
    dispatcher.add_handler(add_test_raid_handler)

    # dispatcher.add_handler(rb.get_raid_bot_handler())

    callback_handler = CallbackQueryHandler(button)
    dispatcher.add_handler(callback_handler)

    recover_handler = CommandHandler('recover', load_state_from_file, filters=Filters.user(s.get_admins()))
    dispatcher.add_handler(recover_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    if s.LULZ:
        lulz_handler = MessageHandler(Filters.text, silence)
        dispatcher.add_handler(lulz_handler)


def pull_api():
    global current_day
    print(time.ctime())
    now = dt.datetime.now()
    sleeptime = 60
    if s.START_TIME <= now.time() < s.END_TIME:
        print("api pull")
        sleeptime = 60
    elif now.time() >= s.END_TIME + s.BUFFER_TIME:
        print("reset raids")
        r.reset_raids()
        sleeptime = (dt.timedelta(hours=24) - (now - now.replace(hour=6, minute=30, second=0, microsecond=0))).total_seconds() % (24 * 3600)
    print("sleeptime is " + str(sleeptime))
    threading.Timer(sleeptime, pull_api).start()


def main():
    updater = Updater(token=s.get_token())
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    add_handlers(dispatcher)
    if s.get_request_method() == "polling":
        updater.start_polling(timeout=25)
        print("Bot started polling!")
    else:
        wh = s.get_webhook_parameters()
        updater.start_webhook(listen=wh["listen"], port=wh["port"], url_path=wh["url_path"], webhook_url=["webhook_url"], cert=wh["cert"], key=wh["key"])
        print("Bot started webhook!")
    # pull_api()


if __name__ == '__main__':
    main()
