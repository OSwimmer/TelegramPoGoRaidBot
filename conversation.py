from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging
import raid as r

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

BOSS, GYM, LOCATION, OPENS = range(4)


def start(bot, update):
    reply_keyboard = [['Mewtwo', 'Snorlax', 'Magikarp', 'Tyranitar']]
    user = update.message.from_user.username
    r.init_user(user)

    update.message.reply_text(
        'Hi! I will help you to add a raid. '
        'Send /cancel to stop talking to me.\n\n'
        'What raid is starting?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return BOSS


def boss(bot, update):
    user = update.message.from_user
    bossname = update.message.text
    r.set_boss(user.username, bossname)
    logger.info("Boss selected by %s: %s", user.first_name, bossname)
    update.message.reply_text('Now send me the name of the gym please.',
                              reply_markup=ReplyKeyboardRemove())

    return GYM


def gym(bot, update):
    user = update.message.from_user
    gymname = update.message.text
    r.set_gym(user.username, gymname)
    logger.info("Gym selected by user %s: %s", user.first_name, gymname)
    update.message.reply_text('Episch! Now, send me the location please')

    return LOCATION


def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    r.set_location(user.username, user_location)
    logger.info("Location of the raid %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Super, now tell me when it opens, with the following format: HH:mm.')

    return OPENS


def opens(bot, update):
    user = update.message.from_user
    username = user.username
    time = update.message.text
    r.set_opentime(username, time)
    logger.info("Open time %s: %s", user.first_name, time)
    update.message.reply_text('Thank you! So to summarize:\n' +
                              r.get_raid_info_as_string(username))
    bot.send_location(chat_id=update.message.chat_id, location=r.get_location(username))
    post_in_group(bot, username)

    return ConversationHandler.END


def post_in_group(bot, username):
    keyboard = [[InlineKeyboardButton("Ik kom! met 0", callback_data='1'),
                 InlineKeyboardButton("Ik kom niet!", callback_data='2')],

                [InlineKeyboardButton("Random knop", callback_data='3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_location(chat_id=r.group_chat_id, location=r.get_location(username))
    bot.send_message(chat_id=r.group_chat_id, text=r.get_raid_info_as_string(username), reply_markup=reply_markup)


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
