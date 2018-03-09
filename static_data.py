import configparser, json, datetime


config = configparser.ConfigParser()
config.read("properties.ini")


# button numbers
ADD_PLAYER_BUTTON_SLOT1 = "1"
ADD_PLAYER_BUTTON_SLOT2 = "2"
ADD_PERSON_BUTTON = "3"
REMOVE_PERSON_BUTTON = "4"
PLAYER_ARRIVED_BUTTON = "5"
REMOVE_PLAYER_BUTTON = "6"

# boss keyboard
MAX_COLUMN_WIDTH = 4

# chat ids
group_chat_id = config["TelegramSettings"]["group_chat_id"]

# icons
TIMESLOT1_ICON = "1️⃣"
TIMESLOT2_ICON = "2️⃣"

# times
START_TIME = datetime.time(hour=8)
END_TIME = datetime.time(hour=21)
BUFFER_TIME = datetime.timedelta(hours=1, minutes=45)
RAID_DURATION = datetime.timedelta(minutes=int(config["GameData"]["raid_duration"]))

# LULZ??
LULZ = False


def reload_config():
    config.read("properties.ini")


def dump_and_reload_config(section, field, value):
    config.set(section, field, value)
    with open("properties.ini", "w+") as configfile:
        config.write(configfile)


def get_token():
    return config["TelegramSettings"]["token"]


def get_moves_file():
    return config["GameData"]["moves_file"]


def get_pokemon_file():
    return config["GameData"]["pokemon_file"]


moves = json.load(open(get_moves_file()))
pokemon = json.load(open(get_pokemon_file()))
region = config["PokeHuntAPI"]["region"]


def get_admins():
    admins = config["TelegramSettings"]["admins"].split(",")
    admins = [int(x) for x in admins]
    return admins


def get_current_raid_bosses():
    bosses = config["GameData"]["current_raid_bosses"].split(", ")
    bosses = [x.capitalize() for x in bosses]
    return bosses


def make_current_bosses_dict():
    bosses = get_current_raid_bosses()
    result = {}
    for boss_id, name in pokemon.items():
        if name in bosses:
            result[name] = boss_id
    return result


current_bosses = make_current_bosses_dict()


def get_raid_backup_file():
    return config["GameData"]["raid_backup_file"]


def get_request_method():
    return config["TelegramSettings"]["request_method"].lower()


def get_webhook_parameters():
    result = {}
    try:
        result["listen"] = config["TelegramSettings"]["listen"]
    except KeyError:
        result["listen"] = '127.0.0.1'
    try:
        result["port"] = int(config["TelegramSettings"]["port"])
    except KeyError:
        result["port"] = 80
    try:
        result["url_path"] = config["TelegramSettings"]["url_path"]
    except KeyError:
        result["url_path"] = ''
    try:
        result["cert"] = config["TelegramSettings"]["cert"]
    except KeyError:
        result["cert"] = None
    try:
        result["key"] = config["TelegramSettings"]["key"]
    except KeyError:
        result["key"] = None
    try:
        result["webhook_url"] = config["TelegramSettings"]["webhook_url"]
    except KeyError:
        result["webhook_url"] = None
    print(str(result))
    return result
