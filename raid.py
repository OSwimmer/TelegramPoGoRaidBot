raids = [
    {
        "boss": "",
        "moveset": [],
        "gym": "",
        "location": "",
        "opens": "",
        "players": {}
    }]
group_chat_id = -201461051
raid_bot_id = -201461051
global_raid_id = 0


def init_raid():
    raids.append({
        "boss": "",
        "moveset": [],
        "gym": "",
        "location": "",
        "opens": "",
        "players": {}
    })


def add_player_to_raid(username, raid_id):
    raids[raid_id]["players"][username] = {
        "persons": 0,
        "coming": True
    }


def add_person_to_player(username, raid_id):
    raids[raid_id]["players"][username]['persons'] += 1


def remove_person_from_player(username, raid_id):
    if raids[raid_id]["players"][username]["persons"] > 0:
        raids[raid_id]["players"][username]["persons"] -= 1


def remove_player_from_raid(username, raid_id):
    raids[raid_id]["players"][username]['coming'] = False


def set_boss(raid_id, boss):
    raids[raid_id]["boss"] = boss


def set_gym(raid_id, gym):
    raids[raid_id]["gym"] = gym


def set_location(raid_id, location):
    raids[raid_id]["location"] = location


def set_opentime(raid_id, time):
    raids[raid_id]["opens"] = time


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


def get_raid_info_as_string(raid_id):
    return (get_boss(raid_id) + ' raid at gym ' + get_gym(raid_id) +
            ' starting at ' + get_opentime(raid_id) +
            '\nPeople joining:\n')


def get_raid_info_with_loc_as_string(raid_id):
    return get_raid_info_as_string(raid_id) + get_location_as_string(raid_id)


def get_players_as_string(raid_id):
    result = ""
    for player in raids[raid_id]["players"]:
        if raids[raid_id]["players"][player]['coming'] is True:
            result = result + "  🔷 " + player
        else:
            result = result + "  ❌ " + player
        persons = raids[raid_id]["players"][player]['persons']
        if persons > 0:
            result = result + " +" + str(persons)
        result = result + "\n"
    return result


def get_full_raid_message(raid_id):
    return get_raid_info_as_string(raid_id) + get_players_as_string(raid_id)
