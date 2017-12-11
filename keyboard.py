from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import raid as r


def get_keyboard(raid_id):
    keyboard = [[InlineKeyboardButton("Ik kom!", callback_data="1," + str(raid_id))],
                [InlineKeyboardButton("Extra speler", callback_data='2,' + str(raid_id)), InlineKeyboardButton("Verwijder speler", callback_data='3,' + str(raid_id))],
                [InlineKeyboardButton("Ik kom niet!", callback_data='4,' + str(raid_id))]]
    return InlineKeyboardMarkup(keyboard)
