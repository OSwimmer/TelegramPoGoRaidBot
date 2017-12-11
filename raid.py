raids = {}
group_chat_id = -201461051


def init_user(user):
    raids[user] = {
        "boss": "",
        "gym": "",
        "location": "",
        "opens": ""
    }


def set_boss(user, boss):
    raids[user]["boss"] = boss


def set_gym(user, gym):
    raids[user]["gym"] = gym


def set_location(user, location):
    raids[user]["location"] = location


def set_opentime(user, time):
    raids[user]["opens"] = time


def get_boss(user):
    return raids[user]["boss"]


def get_gym(user):
    return raids[user]["gym"]


def get_location(user):
    return raids[user]["location"]


def get_location_as_string(user):
    loc = get_location(user)
    return str(loc.latitude) + " / " + str(loc.longitude)


def get_opentime(user):
    return raids[user]["opens"]


def get_raid_info_as_string(user):
    return (get_boss(user) + ' raid at gym ' + get_gym(user) +
            ' starting at ' + get_opentime(user) +
            '\nPeople joining: ')


def get_raid_info_with_loc_as_string(user):
    return get_raid_info_as_string(user) + get_location_as_string(user)
