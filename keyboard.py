from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import static_data as s
import raid as r


def get_keyboard(raid_id):
    data = "," + str(raid_id)
    slots = r.get_timeslots(raid_id)
    keyboard = [[InlineKeyboardButton("%s %s Ik kom!" % (s.TIMESLOT1_ICON, slots[0]), callback_data=s.ADD_PLAYER_BUTTON_SLOT1 + data), InlineKeyboardButton("%s %s Ik kom!" % (s.TIMESLOT2_ICON, slots[1]), callback_data=s.ADD_PLAYER_BUTTON_SLOT2 + data)],
                [InlineKeyboardButton("➕👨 Extra speler", callback_data=s.ADD_PERSON_BUTTON + data), InlineKeyboardButton("➖👨 Verwijder speler", callback_data=s.REMOVE_PERSON_BUTTON + data)],
                [InlineKeyboardButton("🆗 Aanwezig", callback_data=s.PLAYER_ARRIVED_BUTTON + data), InlineKeyboardButton("❌ Ik kom niet!", callback_data=s.REMOVE_PLAYER_BUTTON + data)]]
    return InlineKeyboardMarkup(keyboard)


def get_bosses_keyboard():
    bosses = s.get_current_raid_bosses()
    length = len(bosses)
    rows, remainder = divmod(length, s.MAX_COLUMN_WIDTH)
    result = []
    for row in range(rows):
        start = row * s.MAX_COLUMN_WIDTH
        result.append(bosses[start:start + s.MAX_COLUMN_WIDTH])
    start = rows * s.MAX_COLUMN_WIDTH
    result.append(bosses[start:start + remainder])
    print(str(result))
    return result


def get_time_keyboard():
    keyboard = [['7', '8', '9'],
                ['4', '5', '6'],
                ['1', '2', '3'],
                ['0', ':', "➡"]]
    return keyboard
