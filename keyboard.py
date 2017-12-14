from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import static_data as s


def get_keyboard(raid_id):
    data = "," + str(raid_id)
    keyboard = [[InlineKeyboardButton(s.TIMESLOT1_ICON + " Ik kom!", callback_data=s.ADD_PLAYER_BUTTON_SLOT1 + data), InlineKeyboardButton(s.TIMESLOT2_ICON + " Ik kom!", callback_data=s.ADD_PLAYER_BUTTON_SLOT2 + data)],
                [InlineKeyboardButton("➕👨 Extra speler", callback_data=s.ADD_PERSON_BUTTON + data), InlineKeyboardButton("➖👨 Verwijder speler", callback_data=s.REMOVE_PERSON_BUTTON + data)],
                [InlineKeyboardButton("🆗 Aanwezig", callback_data=s.PLAYER_ARRIVED_BUTTON + data), InlineKeyboardButton("❌ Ik kom niet!", callback_data=s.REMOVE_PLAYER_BUTTON + data)]]
    return InlineKeyboardMarkup(keyboard)
