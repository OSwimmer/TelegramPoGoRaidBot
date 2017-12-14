import static_data as s

raids = [
    {
        "boss": "",
        "moveset": ["Quick", "Fast"],
        "gym": "",
        "location": "",
        "opens": "",
        "timeslots": [],
        "players": {}
    }]
global_raid_id = 0


def init_raid():
    raids.append({
        "boss": "",
        "moveset": ["Quick", "Fast"],
        "gym": "",
        "location": "",
        "opens": "",
        "timeslots": [],
        "players": {}
    })


def add_player_to_raid(username, raid_id, timeslot):
    raids[raid_id]["players"][username] = {
        "persons": 0,
        "coming": True,
        "colour": None,
        "arrived": False,
        "timeslot": timeslot
    }


def add_person_to_player(username, raid_id):
    raids[raid_id]["players"][username]['persons'] += 1


def remove_person_from_player(username, raid_id):
    if raids[raid_id]["players"][username]["persons"] > 0:
        raids[raid_id]["players"][username]["persons"] -= 1


def remove_player_from_raid(username, raid_id):
    raids[raid_id]["players"][username]['coming'] = False
    raids[raid_id]["players"][username]["arrived"] = False


def player_has_arrived(username, raid_id):
    raids[raid_id]["players"][username]["arrived"] = True


def set_boss(raid_id, boss):
    raids[raid_id]["boss"] = boss


def set_gym(raid_id, gym):
    raids[raid_id]["gym"] = gym


def set_location(raid_id, location):
    raids[raid_id]["location"] = location


def set_opentime(raid_id, time):
    raids[raid_id]["opens"] = time


def set_timeslots(raid_id, timeslots):
    raids[raid_id]["timeslots"] = timeslots


def get_timeslots(raid_id):
    return raids[raid_id]["timeslots"]


def set_moveset(raid_id, moveset):
    raids[raid_id]["moveset"] = moveset


def get_moveset(raid_id):
    return raids[raid_id]["moveset"]


def get_boss(raid_id):
    return raids[raid_id]["boss"]


def get_gym(raid_id):
    return raids[raid_id]["gym"]


def get_location(raid_id):
    return raids[raid_id]["location"]


def get_location_as_string(raid_id):
    loc = get_location(raid_id)
    return str(loc.latitude) + " / " + str(loc.longitude)


def get_opentime(raid_id):
    return raids[raid_id]["opens"]


def toBold(string):
    return "*" + string + "*"


def get_raid_info_as_string(raid_id):
    return get_boss_line(raid_id) + get_gym_line(raid_id) + get_time_line(raid_id)


def get_time_line(raid_id):
    result = "Opent om %s\n" % raids[raid_id]["opens"]
    return result


def get_gym_line(raid_id):
    gym = get_gym(raid_id)
    result = "Gym naam: %s\n" % (gym)
    return result


def get_boss_line(raid_id):
    moveset = get_moveset(raid_id)
    quick_move = moveset[0]
    charged_move = moveset[1]
    result = "%s (%s / %s) Raid\n" % (toBold(get_boss(raid_id)), quick_move, charged_move)
    return result


def get_raid_info_with_loc_as_string(raid_id):
    return get_raid_info_as_string(raid_id) + get_location_as_string(raid_id)


def timeslot_to_icon_string(raid_id, user, slot):
    if slot is 0:
        return s.TIMESLOT1_ICON
    else:
        return s.TIMESLOT2_ICON


def slots_to_string(slots, slot1, slot2):
    return "  Moment %s %s:\n%s\n  Moment %s %s:\n%s" % (s.TIMESLOT1_ICON, slots[0], slot1, s.TIMESLOT2_ICON, slots[1], slot2)


def get_players_as_string(raid_id):
    result = "\nSpelers die komen:\n"
    players_coming = [0, 0]
    players_arrived = [0, 0]
    slot1 = ""
    slot2 = ""
    for player in raids[raid_id]["players"]:
        coming = raids[raid_id]["players"][player]['coming']
        slot = raids[raid_id]["players"][player]["timeslot"]
        if coming is True:
            line = "   %s %s" % ("└", player)
            players_coming[slot] += 1
        else:
            line = "   ❌ " + player
        persons = raids[raid_id]["players"][player]['persons']
        if persons > 0:
            line = line + " +" + str(persons)
        arrived = raids[raid_id]["players"][player]['arrived']
        if arrived is True and coming is True:
            line = line + "  🆗"
            players_arrived[slot] += 1
        line = line + "\n"
        if slot is 0:
            slot1 = slot1 + line
        else:
            slot2 = slot2 + line
    slots = get_timeslots(raid_id)
    result = result + slots_to_string(slots, slot1, slot2)
    return result, players_coming[0] - players_arrived[0], players_coming[1] - players_arrived[1]


def get_can_start_message(diff, slot_icon):
    can_start = "\n%s " % slot_icon
    if diff <= 0:
        can_start = can_start + toBold("Iedereen is aanwezig!")
    elif diff == 1:
        can_start = can_start + "Er moet nog *één* iemand komen"
    else:
        can_start = can_start + "Er moeten nog " + toBold(str(diff)) + " spelers komen"
    return can_start


def get_full_raid_message(raid_id):
    players, diff1, diff2 = get_players_as_string(raid_id)
    return get_raid_info_as_string(raid_id) + players + get_can_start_message(diff1, s.TIMESLOT1_ICON) + get_can_start_message(diff2, s.TIMESLOT2_ICON)
