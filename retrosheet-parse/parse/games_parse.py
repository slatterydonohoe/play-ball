#!/usr/bin/env python
import csv
import sys

filepath = "/Users/slatterydonohoe/Downloads/2018eve/"

game_ids = [
    'ANA201804020',
    'ANA201804030',
    'ANA201804040',
    'ANA201804060',
    'ANA201804070',
    'ANA201804080',
    'ANA201804170',
    'ANA201804180',
    'ANA201804190',
    'ANA201804200',
    'ANA201804210',
    'ANA201804220',
    'ANA201804270',
    'ANA201804280',
    'ANA201804290'
]

events = [
    'K',
    'G',
    'F',
    'L',
    'SF',
    'FO',
    'FC',
    'GDP',
    'LDP',
    'GTP',
    'LTP',
    'S',
    'D',
    'T',
    'DGR',
    'FC',
    'FLE',
    'H',
    'HR',


]

def parse_result(res):
    res_elements = res.split('/')
    desc = res_elements[0]
    outs = 0
    mod = res_elements[-1] if len(res_elements) > 1 else desc
    field_event = mod.split('.')[0]
    field_play = mod.split('.')[1] if len(mod.split('.')) > 1 else ""
    if len(res_elements) > 1:
        # triple play
        if any(x in res for x in ['GTP', 'LTP', '/TP']):
            return 3
        # double play
        elif any(x in res for x in ['GDP', 'LDP', '/DP']):
            return 2
        # all other outs
        elif field_event in events[4:6] or desc[0].isdigit():
            outs += 1
    if desc[0] == 'K':
        outs += 1
    # outs in the field
    outs += field_play.count('X')
    # caught stealing
    outs += desc.count('CS')
    return outs
    # regex for matching outs


def parse_play(play):
    inning = play[1]
    home = play[2] == 1
    player_id = play[3]
    count = play[4]
    pitches = play[5]
    result = play[6]
    return parse_result(result)


def parse_game(reader, game_id):
    outs = 0
    inning_outs = 0
    inning = '1'
    top = '0'
    found_game = False
    for row in reader:
        # process game ID row
        if row[0] == "id":
            # Found the game we want
            if row[1] == game_id:
                found_game = True
            # Found game we don't want, but if we already found our game, this means we are done
            elif found_game:
                break
        # process play row
        elif found_game and ((row[0] == "play" and found_game) or row[0] == "data"):
            # log half-inning
            if inning != row[1] or top != row[2]:
                print("Outs for " + ("top " if top == '0' else "bot ") + str(inning) + ": " + str(inning_outs))
                if row[0] == "play":
                    inning = row[1]
                    top = row[2]
                    inning_outs = 0
            if row[0] == "data":
                break
            else:
                row_outs = parse_play(row)
                outs += row_outs
                inning_outs += row_outs
    print("Outs for game " + game_id + ": " + str(outs))


def parse_file(file, game_id):
    with open(file) as season_file:
        season_reader = csv.reader(season_file, delimiter=',')
        parse_game(season_reader, game_id)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        for g in game_ids:
            parse_file(sys.argv[1], g)
    else:
        parse_file(sys.argv[1], sys.argv[2])
