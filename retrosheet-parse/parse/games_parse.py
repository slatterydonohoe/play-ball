#!/usr/bin/env python
import csv
import sys

filepath = "/Users/slatterydonohoe/Downloads/2018eve/"

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

#def parse_out(res):
#    res_elements = res.split("/")
#    play = ""
#    outs = 0
#    if len(res_elements) > 1:
#        #if res_elements[1] in events[:10]:
#        #    play = res_elements[1]
#       if res_elements[1] in events[9:11]:
#            outs += 3
#        if res_elements[1] in events[7:9]:
#            outs += 2
#        if res_elements[1] in events[4:6] or res_elements[0][0].isdigit():
#            outs += 1
#    if res == "K":
#        outs += 1
#
#    return outs


def parse_result(res):
    res_elements = res.split('/')
    desc = res_elements[0]
    outs = 0
    mod = res_elements[-1] if len(res_elements) > 1 else ""
    field_event = mod.split('.')[0]
    field_play = mod.split('.')[1] if len(mod.split('.')) > 1 else ""
    if len(res_elements) > 1:
        # triple play
        if field_event in events[9:11]:
            outs += 3
        # double play
        elif field_event in events[7:9]:
            outs += 2
        # all other outs
        elif field_event in events[4:6] or desc[0].isdigit():
            outs += 1
    elif desc[0] == 'K':
        outs += 1
    # outs in the field

    outs += field_play.count('X')
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


def parse_file(file, game_id):
    with open(file) as season_file:
        season_reader = csv.reader(season_file, delimiter=',')
        outs = 0
        inning_outs = 0
        inning = '1'
        top = '0'
        found_game = False
        for row in season_reader:
            # process game ID row
            if row[0] == "id":
                # Found the game we want
                if row[1] == game_id:
                    found_game = True
                # Found game we don't want, but if we already found our game, this means we are done
                elif found_game:
                    break
            # process play row
            elif row[0] == "play" and found_game:
                # log half-inning
                if inning != row[1] or top != row[2]:
                    print("Outs for " + ("top " if top == '0' else "bottom ") + str(inning) + ": " + str(inning_outs))
                    inning = row[1]
                    top = row[2]
                    inning_outs = 0
                row_outs = parse_play(row)
                outs += row_outs
                inning_outs += row_outs
        print("Outs for game " + game_id + ": " + str(outs))



if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("ERROR: Missing filename or game ID")
    else:
        parse_file(sys.argv[1], sys.argv[2])
