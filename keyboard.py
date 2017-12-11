from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def get_keyboard():
    keyboard = [[InlineKeyboardButton("Ik kom!", callback_data='1')],
                [InlineKeyboardButton("Extra speler", callback_data='2'), InlineKeyboardButton("Verwijder speler", callback_data='3')],
                [InlineKeyboardButton("Ik kom niet!", callback_data='4')]]
    return InlineKeyboardMarkup(keyboard)
