#!/usr/bin/env python
import csv
import re
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

events = [ #
    'K', # strikeout
    'W', # walk
    'IW', # intentional walk
    'HP', # hit by pitch
    'E', # error
    'G', # grounder
    'F', # fly
    'P', # popup
    'L', # line drive
    'SF', # sac fly
    'FC', # fielder's choice
    'S', # single
    'D', # double
    'T', # triple
    'H', # homer
    'HR', # homer
    'DGR', # ground rule double
    'FLE', # fly ball error
    # 'DP', # double play
    'GDP', # grounder double play
    'LDP', # liner double play
    # 'TP', # triple play
    'GTP', # grounder triple play
    'LTP', # liner triple play
    # extras I don't care about
    'PO', # picked off
    'POCS', # picked off caught stealing
    'BG', # ground ball bunt
    # 'DI', # defensive indifference
    'OA' # other runner's advance not covered by codes
]

regex = '^[A-Z]+'


def parse_result(result):
    res_elements = result.split('/')
    desc = res_elements[0]
    outs = 0
    # Play class values
    #game_id
    #batter_id
    #pitcher_id
    #balls
    #strikes
    on_1B = ''
    on_2B = ''
    on_3B = ''
    play = ''
    finished_1B = 0
    finished_2B = 0
    finished_3B = 0
    mod = desc
    r1 = re.findall(regex, mod)
    if len(res_elements) > 1:
        mod = res_elements[-1]

    # field_event = mod.split('.')[0]
    #field_play = mod.split('.')[1] if len(mod.split('.')) > 1 else ""

    # field out
    if not(len(r1) > 0 and r1[0] in events) and desc[0].isdigit() and len(res_elements) > 1:
        r1 = re.findall(regex, mod)
        if not(len(r1) > 0 and r1[0] in events) and len(res_elements) > 2:
            mod = res_elements[-2]
            r1 = re.findall(regex, mod)
    if len(r1) > 0 and r1[0] in events:
        play = r1[0]
    # else:
    #    mod = res_elements[-2]
    #    r1 = re.findall(regex, mod)

    else:
        print("WHAT THE FUCK")

    #if len(res_elements) > 1:
        # triple play
    #    if any(x in res for x in ['GTP', 'LTP', '/TP']):
    #        if result == '':
    #            result = 'TP'
    #        outs = 3
    #    # double play
    #    elif any(x in res for x in ['GDP', 'LDP', '/DP']):
    #        if result == '':
    #            result = 'DP'
    #        outs = 2
    #    # all other outs
    #    # elif field_event in events[4:6] or \
    #    elif desc[0].isdigit():
    #        outs += 1

    # outs in the field
    #outs += field_play.count('X')
    # caught stealing
    outs += desc.count('CS')
    return play
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
    hits = 0
    inning_hits = 0
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
        elif found_game and (row[0] == "play" or row[0] == "data"):
            # log half-inning
            if inning != row[1] or top != row[2]:
                print("Hits for " + ("top " if top == '0' else "bot ") + str(inning) + ": " + str(inning_hits))
                if row[0] == "play":
                    inning = row[1]
                    top = row[2]
                    inning_hits = 0
            if row[0] == "data":
                break
            # ignore no-plays, steals/caught stealing/def indifference, and passed ball/ wild pitch
            elif row[6] == "NP" or any(re.match(x, row[6]) for x in ['^CS', '^SB', '^DI', '^WP', '^PB']):
                continue
            else:
                row_event = parse_play(row)
                if row_event in ['S', 'D', 'T', 'HR', 'H', 'DGR'] and top == '1':
                    hits += 1
                    inning_hits += 1
    print("Hits for game " + game_id + ": " + str(hits))


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
