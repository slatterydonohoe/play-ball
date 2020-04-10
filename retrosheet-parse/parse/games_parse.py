#!/usr/bin/env python3.7
import csv
import mysql.connector
import re
import sys

from play import Play
import credentials

filepath = "/Users/slatterydonohoe/Downloads/2018eve/"

events = [  #
    'K',  # strikeout
    'K+SB',
    'K+CS',
    'K+PO',
    'K+E',
    'W',  # walk
    'W+SB',
    'W+CS',
    'W+PO',
    'W+E',
    'IW',  # intentional walk
    'IW+SB',
    'IW+CS',
    'IW+PO',
    'IW+E',
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
    # base running
    'PO',  # picked off
    'BK',  # balk
    'SB',  # stolen base
    'CS',  # caught stealing
    'POCS',  # picked off caught stealing
    'BG',  # ground ball bunt
    'PB',  # passed ball
    'WP',  # wild pitch
    'DI',  # defensive indifference
    'OA'  # other runner's advance not covered by codes
]

event_regex = r'^[A-Z]+\+*[A-Z]*'


# Class to parse play-by-play data from Retrosheet data files
# Description of files: https://www.retrosheet.org/eventfile.htm
class GamesParse:
    onBases = ['', '', '', '']
    cnx = mysql.connector.connect(user=credentials.sql['user'],
                                  password=credentials.sql['password'],
                                  database='mlb',
                                  auth_plugin='mysql_native_password')

    @staticmethod
    def send_play_to_db(play):
        cursor = GamesParse.cnx.cursor()
        args = (play.game_id, play.play_id, play.batter_id, play.pitcher_id, play.home, play.balls, play.strikes,
                play.on_1B, play.on_2B, play.on_3B, play.result,
                play.finished_H, play.finished_1B, play.finished_2B, play.finished_3B)
        try:
            cursor.callproc('add_play', args)
        except mysql.connector.Error as error:
            print("Failed to execute stored procedure: {}".format(error))

    @staticmethod
    def send_game_to_db(game_id, away, home):
        cursor = GamesParse.cnx.cursor()
        try:
            cursor.callproc('add_game', [game_id, away, home, ])
        except mysql.connector.Error as error:
            print("Failed to execute stored procedure: {}".format(error))

    @staticmethod
    def parse_result(result, game, play_num, player, home):
        res_elements = result.split('/')
        desc = res_elements[0]
        play_id = ''
        outs = 0
        finished_at_bases = [0, 0, 0, 0]  # -1: out, 0: not on base, 4: scored

        mod = desc
        r1 = re.findall(event_regex, mod)
        if len(res_elements) > 1:
            mod = res_elements[-1]

        # find event if field out
        if not (len(r1) > 0 and r1[0] in events) and desc[0].isdigit() and len(res_elements) > 1:
            r1 = re.findall(event_regex, mod)
            if not (len(r1) > 0 and r1[0] in events) and len(res_elements) > 2:
                mod = res_elements[-2]
                r1 = re.findall(event_regex, mod)
        if len(r1) > 0 and r1[0] in events:
            play_id = r1[0]

        # initialize finished_at_bases values
        for runner in GamesParse.onBases:
            if len(runner) > 0 and runner != GamesParse.onBases[0]:
                index = GamesParse.onBases.index(runner)
                finished_at_bases[index] = index

        # handle strikeout/walk plus baserunning
        if play_id[:2] in ['K+', 'W+'] and play_id[2:] in ['SB', 'CS', 'OA', 'PO'] or play_id[:3] == 'IW+':
            # cache current runners on base
            temp_on_bases = GamesParse.onBases
            run_result = result[result.index('+') + 1:]
            # recurse on running events  and only process batter event moving forward
            (run_play, run_outs, run_only) = GamesParse.parse_result(run_result, game, play_num, player, home)
            finished_at_bases[1] = run_play.finished_1B
            finished_at_bases[2] = run_play.finished_2B
            finished_at_bases[3] = run_play.finished_3B
            result = play_id
            # replace modified on base values with cached values
            GamesParse.onBases = temp_on_bases

        # identify baserunning
        baserunning_only = play_id in ['CS', 'SB', 'DI', 'WP', 'PB', 'BK']
        # base movement
        if play_id in ['S', 'W', 'IW', 'E', 'HP', 'FLE', 'FC'] or any(result.find(x) > -1 for x in ['/FO/', 'K+PB', 'K+WP']):
            finished_at_bases[0] = 1
        elif play_id in ['D', 'DGR']:
            finished_at_bases[0] = 2
        elif play_id == 'T':
            finished_at_bases[0] = 3
        elif play_id == 'HR':
            finished_at_bases[0] = 4
        elif not baserunning_only:
            finished_at_bases[0] = -1

        # replace home and batter with digits
        base_mod_result = result.replace('B', '0').replace('H', '4')

        # out/advance from steal/caught stealing/picked off
        if play_id == 'SB':
            finished_at_bases[int(result[2]) - 1] = int(result[2])
        elif play_id == 'CS' or play_id == 'POCS':
            index = len(play_id)
            finished_at_bases[int(result[index]) - 1] = -1
        elif play_id == 'PO':
            finished_at_bases[int(result[index])] = -1

        # runners advance, ex. 1-3 runner at first advances to third
        r2 = re.findall(r'[0123]-[1234]', base_mod_result)
        for adv in r2:
            finished_at_bases[int(adv[0])] = int(adv[2])

        # explicit outs in the field, ex. (1)
        r3 = re.findall(r'\([0123]\)', base_mod_result)
        for out in r3:
            finished_at_bases[int(out[1])] = -1

        # outs on the basepaths, ex. 2X4(82) runner at second thrown out at home, from CF to catcher
        # descriptions of fielders with "E" indicate safe on error - 2X4(8E2) runner safe at home, throwing error by CF
        r4 = re.findall(r'[0123]X[1234]', base_mod_result)
        for out in r4:
            out_pos = base_mod_result.index(out)
            r4 = re.findall(r'^\([0-9]+E*[0-9]\)', base_mod_result[out_pos + len(out):])
            if len(r4) == 1:
                if r4[0].find('E') > 0:
                    finished_at_bases[int(out[0])] = int(out[2])
                else:
                    finished_at_bases[int(out[0])] = -1

        play = Play(game, play_num, player, '', home, 0, 0,
                    GamesParse.onBases[1], GamesParse.onBases[2], GamesParse.onBases[3],
                    play_id,
                    finished_at_bases[0],
                    finished_at_bases[1],
                    finished_at_bases[2],
                    finished_at_bases[3])

        # set current on-base ids
        temp_on_bases = list(GamesParse.onBases)
        GamesParse.onBases = ['', '', '', '']
        for x in finished_at_bases:
            if x in [1, 2, 3]:
                GamesParse.onBases[x] = temp_on_bases[finished_at_bases.index(x)]
        outs = finished_at_bases.count(-1)
        return play, outs, baserunning_only

    @staticmethod
    def parse_play(play, game, play_id):
        inning = int(play[1])
        home = play[2] == '1'
        player_id = play[3]
        count = play[4]
        result = play[6]
        GamesParse.onBases[0] = player_id
        (play, outs, baserunning_only) = GamesParse.parse_result(result, game, play_id, player_id, home)
        if not baserunning_only:
            play.inning = inning
            play.home = home
            play.balls = int(count[0])
            play.strikes = int(count[1])
        return play, outs, baserunning_only

    @staticmethod
    def parse_game(reader, game_id):
        hits = 0
        outs = 0
        inning_hits = 0
        inning_outs = 0
        inning = '1'
        top = '0'
        play_id = 1
        found_game = False
        vis_id = ''
        home_id = ''
        plays = []
        for row in reader:

            # process game ID row
            if row[0] == "id":
                # Found the game we want
                if row[1] == game_id:
                    found_game = True
                # Found game we don't want, but if we already found our game, this means we are done
                elif found_game:
                    break
            # get game-level info and send to DB
            elif found_game and row[0] == "info":
                if row[1] == "visteam":
                    vis_id = row[2]
                elif row[1] == "hometeam":
                    home_id = row[2]
            # process play row
            elif found_game and (row[0] == "play" or row[0] == "data"):
                # log half-inning
                if inning != row[1] or top != row[2]:
                    GamesParse.onBases = ['', '', '', '']
                    if row[0] == "play":
                        if top == '1':
                            print("Outs for inning " + inning + ": " + str(inning_outs))
                        inning = row[1]
                        top = row[2]
                        inning_hits = 0
                        inning_outs = 0
                if row[0] == "data":
                    break
                # ignore no-plays
                elif row[6] == 'NP':  # or any(re.match(x, row[6]) for x in ['^CS', '^SB', '^DI', '^WP', '^PB']):
                    continue
                else:
                    (row_event, play_outs, baserunning_only) = GamesParse.parse_play(row, game_id, play_id)
                    if not baserunning_only:
                        play_id += 1
                    if top == '1':
                        outs += play_outs
                        inning_outs += play_outs
                        if not baserunning_only:
                            plays.append(row_event)
                            if row_event.result in ['S', 'D', 'T', 'HR', 'H', 'DGR']:
                                hits += 1
                                inning_hits += 1
        return vis_id, home_id, hits, outs, plays

    @staticmethod
    def parse_file_for_game(file, game_id):
        with open(file) as season_file:
            season_reader = csv.reader(season_file, delimiter=',')
            data = GamesParse.parse_game(season_reader, game_id)
            season_file.close()
            return data

    @staticmethod
    def parse_file_for_all_games(file):
        # read the file once, get all game IDs, call parse_file_for_game() on each ID
        # THIS IS NOT EFFICIENT: Need better structured code eventually, using brute force for MVP
        ids = []
        with open(file) as season_file:
            season_reader = csv.reader(season_file, delimiter=',')
            for row in season_reader:
                if row[0] == 'id':
                    ids.append(row[1])
            season_file.close()
        for game in ids:
            (vis, home, hits, outs, plays) = GamesParse.parse_file_for_game(file, game)
            GamesParse.send_game_to_db(game, vis, home)
            for p in plays:
                GamesParse.send_play_to_db(p)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        (vis_team, home_team, game_hits, game_outs, game_plays) = GamesParse.parse_file_for_game(sys.argv[1], sys.argv[2])
        GamesParse.send_game_to_db(sys.argv[2], vis_team, home_team)
        GamesParse.cnx.close()
    elif len(sys.argv) == 2:
        GamesParse.parse_file_for_all_games(sys.argv[1])
