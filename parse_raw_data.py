import json
import static_data as s


def parse_moves():
    moves = json.load(open('moves.json'))
    moves_dict = {}

    for id in moves:
        moves_dict[id] = moves[id]["name"]

    with open(s.get_moves_file(), 'w') as outfile:
        json.dump(moves_dict, outfile)


def parse_pokemon():
    pokemon = json.load(open('pokemon.json'))
    moves_pokemon = {}

    for id in pokemon:
        moves_pokemon[id] = pokemon[id]["name"]

    with open(s.get_pokemon_file(), 'w') as outfile:
        json.dump(moves_pokemon, outfile)


parse_moves()
parse_pokemon()
