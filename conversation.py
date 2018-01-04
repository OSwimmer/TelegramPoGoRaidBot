from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import time
import datetime as dt
import logging
import raid as r
import static_data as s
from keyboard import get_keyboard, get_bosses_keyboard, get_time_keyboard

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

BOSS, GYM, LOCATION, OPENS = range(4)


def start(bot, update):
    reply_keyboard = get_bosses_keyboard()
    user = update.message.from_user.username
    r.init_raid()

    update.message.reply_text(
        'Hallo! Ik zal je helpen om een raid toe te voegen. '
        'Stuur /cancel op elk moment om te stoppen.\n\n'
        'Welke raid gaat starten?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return BOSS


def boss(bot, update):
    user = update.message.from_user
    bossname = update.message.text
    r.set_boss_by_name(r.global_raid_id, bossname)
    logger.info("Boss selected by %s: %s", user.first_name, bossname)
    update.message.reply_text('Wat is de naam van de gym?',
                              reply_markup=ReplyKeyboardRemove())
    return GYM


def gym(bot, update):
    user = update.message.from_user
    gymname = update.message.text
    r.set_gym(r.global_raid_id, gymname)
    logger.info("Gym selected by user %s: %s", user.first_name, gymname)
    update.message.reply_text('Episch! Stuur me de locatie van de raid aub.')

    return LOCATION


def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    r.set_location_with_object(r.global_raid_id, user_location)
    logger.info("Location of the raid %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Super, wanneer start de raid en gebruik het volgende formaat: hh:mm(:ss).')
    return OPENS


def opens(bot, update):
    user = update.message.from_user
    message = update.message
    time_str = message.text
    time_obj = r.parse_time_string(time_str)
    if time_obj is None:
        bot.send_message(chat_id=update.message.chat_id, text="Dat is geen correct formaat, gebruik dit aub: HH:mm(:ss).")
        return OPENS
    r.set_opentime(r.global_raid_id, time_str)
    slot1, slot2 = r.calculate_timeslots(time_obj)
    r.set_timeslots(r.global_raid_id, [slot1, slot2])
    logger.info("Open time %s: %s", user.first_name, time_str)
    update.message.reply_text('Bedankt! Dus om samen te vatten:\n' +
                              r.get_raid_info_as_string(r.global_raid_id), parse_mode=ParseMode.MARKDOWN)
    bot.send_location(chat_id=update.message.chat_id, location=r.get_location_as_object(r.global_raid_id))
    post_in_group(bot)
    r.increment_global_raid_id()
    r.save_raids_to_file()

    return ConversationHandler.END


def post_in_group(bot):
    reply_markup = get_keyboard(r.global_raid_id)
    bot.send_location(chat_id=s.group_chat_id, location=r.get_location_as_object(r.global_raid_id))
    bot.send_message(chat_id=s.group_chat_id, text=r.get_raid_info_as_string(r.global_raid_id), reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Toevoegen van een raid is geannuleerd!',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def get_add_raid_handler():
    # Add conversation handler with the states BOSS, GYM, LOCATION and OPENS
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(command='addRaid', callback=start, filters=Filters.user(s.get_admins()))],

        states={
            BOSS: [RegexHandler('^(' + "|".join(s.get_current_raid_bosses()) + ')$', boss)],

            GYM: [MessageHandler(Filters.text, gym)],

            LOCATION: [MessageHandler(Filters.location, location)],

            OPENS: [MessageHandler(Filters.text, opens)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return conv_handler
