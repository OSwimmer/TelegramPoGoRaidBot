from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def get_keyboard():
    keyboard = [[InlineKeyboardButton("Ik kom!\nMet 10", callback_data='1'),
                 InlineKeyboardButton("Ik kom niet!", callback_data='2')],

                [InlineKeyboardButton("Random knop", callback_data='3')]]
    return InlineKeyboardMarkup(keyboard)
