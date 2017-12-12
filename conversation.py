from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import time
import logging
import raid as r
from keyboard import get_keyboard

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

BOSS, GYM, LOCATION, OPENS = range(4)


def start(bot, update):
    reply_keyboard = [['Mewtwo', 'Snorlax', 'Magikarp', 'Tyranitar']]
    user = update.message.from_user.username
    r.init_raid()

    update.message.reply_text(
        'Hi! I will help you to add a raid. '
        'Send /cancel to stop talking to me.\n\n'
        'What raid is starting?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return BOSS


def boss(bot, update):
    user = update.message.from_user
    bossname = update.message.text
    r.set_boss(r.global_raid_id, bossname)
    logger.info("Boss selected by %s: %s", user.first_name, bossname)
    update.message.reply_text('Now send me the name of the gym please.',
                              reply_markup=ReplyKeyboardRemove())

    return GYM


def gym(bot, update):
    user = update.message.from_user
    gymname = update.message.text
    r.set_gym(r.global_raid_id, gymname)
    logger.info("Gym selected by user %s: %s", user.first_name, gymname)
    update.message.reply_text('Episch! Now, send me the location please')

    return LOCATION


def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    r.set_location(r.global_raid_id, user_location)
    logger.info("Location of the raid %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Super, now tell me when it opens, with the following format: HH:mm.')

    return OPENS


def opens(bot, update):
    user = update.message.from_user
    username = user.username
    try:
        time_obj = time.strptime(update.message.text, '%H:%M')
        time_str = time.strftime('%H:%M', time_obj)
    except ValueError:
        bot.send_message(chat_id=update.message.chat_id, text="That is not a valid time format, please use HH:mm.")
        return OPENS
    r.set_opentime(r.global_raid_id, time_str)
    logger.info("Open time %s: %s", user.first_name, time_str)
    update.message.reply_text('Thank you! So to summarize:\n' +
                              r.get_raid_info_as_string(r.global_raid_id))
    bot.send_location(chat_id=update.message.chat_id, location=r.get_location(r.global_raid_id))
    post_in_group(bot)
    r.global_raid_id += 1

    return ConversationHandler.END


def post_in_group(bot):
    reply_markup = get_keyboard(r.global_raid_id)
    bot.send_location(chat_id=r.group_chat_id, location=r.get_location(r.global_raid_id))
    bot.send_message(chat_id=r.group_chat_id, text=r.get_raid_info_as_string(r.global_raid_id), reply_markup=reply_markup)


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def get_add_raid_handler():
    # Add conversation handler with the states BOSS, GYM, LOCATION and OPENS
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('addRaid', start)],

        states={
            BOSS: [RegexHandler('^(Mewtwo|Snorlax|Magikarp|Tyranitar)$', boss)],

            GYM: [MessageHandler(Filters.text, gym)],

            LOCATION: [MessageHandler(Filters.location, location)],

            OPENS: [MessageHandler(Filters.text, opens)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return conv_handler
