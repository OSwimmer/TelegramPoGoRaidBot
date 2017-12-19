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

# chat ids
group_chat_id = config["TelegramSettings"]["group_chat_id"]
raid_bot_id = -201461051

# icons
TIMESLOT1_ICON = "1️⃣"
TIMESLOT2_ICON = "2️⃣"


# times
START_TIME = datetime.time(hour=8)
END_TIME = datetime.time(hour=21)
BUFFER_TIME = datetime.timedelta(hours=1, minutes=45)


def get_token():
    return config["TelegramSettings"]["token"]


def get_moves_file():
    return config["GameData"]["moves_file"]


def get_pokemon_file():
    return config["GameData"]["pokemon_file"]


moves = json.load(open(get_moves_file()))
pokemon = json.load(open(get_pokemon_file()))
region = config["PokeHuntAPI"]["region"]
