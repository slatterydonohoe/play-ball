#!/usr/bin/env python
import csv
import re
import sys
from play import Play

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

events = [  #
    'K',  # strikeout
    'W',  # walk
    'IW',  # intentional walk
    'HP',  # hit by pitch
    'E',  # error
    'G',  # grounder
    'F',  # fly
    'P',  # popup
    'L',  # line drive
    'SF',  # sac fly
    'FC',  # fielder's choice
    'S',  # single
    'D',  # double
    'T',  # triple
    'H',  # homer
    'HR',  # homer
    'DGR',  # ground rule double
    'FLE',  # fly ball error
    # 'DP',  # double play
    'GDP',  # grounder double play
    'LDP',  # liner double play
    # 'TP', # triple play
    'GTP',  # grounder triple play
    'LTP',  # liner triple play
    # extras I don't care about
    'PO',  # picked off
    'POCS',  # picked off caught stealing
    'BG',  # ground ball bunt
    # 'DI', # defensive indifference
    'OA'  # other runner's advance not covered by codes
]

event_regex = '^[A-Z]+'


class GamesParse:
    onBases = ['', '', '', '']
    @staticmethod
    def parse_result(result, game, player):
        res_elements = result.split('/')
        desc = res_elements[0]
        outs = 0
        play = ''
        finishedAtBases = [-1, 0, 0, 0]  # -1: out, 0: not on base, 4: scored
        # initialize finishedAtBases values
        for runner in GamesParse.onBases:
            if len(runner) > 0 and runner != GamesParse.onBases[0]:
                index = GamesParse.onBases.index(runner)
                finishedAtBases[index] = index
        mod = desc
        r1 = re.findall(event_regex, mod)
        if len(res_elements) > 1:
            mod = res_elements[-1]

        # field out
        if not(len(r1) > 0 and r1[0] in events) and desc[0].isdigit() and len(res_elements) > 1:
            r1 = re.findall(event_regex, mod)
            if not(len(r1) > 0 and r1[0] in events) and len(res_elements) > 2:
                mod = res_elements[-2]
                r1 = re.findall(event_regex, mod)
        if len(r1) > 0 and r1[0] in events:
            play = r1[0]

        else:
            print("WHAT THE FUCK")
        # base movement
        if play in ['S', 'W', 'IW', 'E', 'HP'] or any(result.find(x) > -1 for x in ['/FO/', 'K+PB', 'K+WP']):
            finishedAtBases[0] = 1
        elif play in ['D', 'DGR']:
            finishedAtBases[0] = 2
        elif play == 'T':
            finishedAtBases[0] = 3
        elif play == 'HR':
            finishedAtBases[0] = 4
        else:
            outs += 1
        # runners advance
        baseModResult = result.replace('B', '0').replace('H', '4')
        r2 = re.findall('[0123]-[1234]', baseModResult)
        for adv in r2:
            finishedAtBases[int(adv[0])] = int(adv[2])
        # explicit outs in the field
        r3 = re.findall(r'\([0123]\)', baseModResult)
        for out in r3:
            finishedAtBases[int(out[1])] = -1
            outs += 1
        # outs on the basepaths
        r4 = re.findall("[0123]X[1234]", baseModResult)
        for out in r4:
            outPos = baseModResult.index(out)
            blah = baseModResult[outPos + len(out):]
            r4 = re.findall('^\([0-9]+E*[0-9]\)', baseModResult[outPos + len(out):])
            if len(r4) == 1:
                if r4[0].find('E') > 0:
                    finishedAtBases[int(out[0])] = int(out[2])
                else:
                    finishedAtBases[int(out[0])] = -1
                    outs += 1

        playObj = Play(game, player, '', '', '',
                       GamesParse.onBases[1], GamesParse.onBases[2], GamesParse.onBases[3],
                       play,
                       finishedAtBases[0],
                       finishedAtBases[1],
                       finishedAtBases[2],
                       finishedAtBases[3])
        # set current on-base ids
        tempOnBases = list(GamesParse.onBases)
        for x in finishedAtBases:
            if x in [1, 2, 3]:
                GamesParse.onBases[x] = tempOnBases[finishedAtBases.index(x)]
        return play, outs
        # regex for matching outs

    @staticmethod
    def parse_play(play, game):
        inning = play[1]
        home = play[2] == '1'
        player_id = play[3]
        count = play[4]
        pitches = play[5]
        result = play[6]
        GamesParse.onBases[0] = player_id
        return GamesParse.parse_result(result, game, player_id)

    @staticmethod
    def parse_game(reader, game_id):
        hits = 0
        outs = 0
        inning_hits = 0
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
            elif found_game and (row[0] == "play" or row[0] == "data"):
                # log half-inning
                if inning != row[1] or top != row[2]:
                    GamesParse.onBases = ['', '', '', '']
                    if row[0] == "play":
                        inning = row[1]
                        top = row[2]
                        inning_hits = 0
                        inning_outs = 0
                if row[0] == "data":
                    break
                # ignore no-plays, steals/caught stealing/def indifference, and passed ball/ wild pitch
                elif row[6] == "NP" or any(re.match(x, row[6]) for x in ['^CS', '^SB', '^DI', '^WP', '^PB']):
                    continue
                elif top == '1':
                    (row_event, play_outs) = GamesParse.parse_play(row, game_id)
                    outs += play_outs
                    inning_outs += play_outs
                    if row_event in ['S', 'D', 'T', 'HR', 'H', 'DGR']:
                        hits += 1
                        inning_hits += 1
        print("Hits for game " + game_id + ": " + str(hits))
        print("Outs for game " + game_id + ": " + str(outs))
        return (hits, outs)

    @staticmethod
    def parse_file(file, game_id):
        with open(file) as season_file:
            season_reader = csv.reader(season_file, delimiter=',')
            return GamesParse.parse_game(season_reader, game_id)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        for g in game_ids:
            GamesParse.parse_file(sys.argv[1], g)
    else:
        GamesParse.parse_file(sys.argv[1], sys.argv[2])
