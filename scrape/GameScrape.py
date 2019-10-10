import requests
from bs4 import BeautifulSoup
import re
import ast
import json
from data import Play


class GameScrape:
    def create_play(self, play_row, away_players, home_players):
        start_quote = play_row.find("'")
        end_quote = play_row.find("'", start_quote + 1)
        play_str = play_row[start_quote + 1: end_quote]
        start_b = play_str.find("<b>")
        end_b = play_str.find("</b>")
        play_timing = play_str[start_b + 3:end_b].split(", ")
        play_segments = play_str[play_str.find("<br>") + 4:].split("<br>")
        # variables to construct play
        on1B = self.on1B
        on2B = self.on2B
        on3B = self.on3B
        # play_timing[0]: "side inning"
        top = play_timing[0].find("Top") > -1
        inning = int(play_timing[0].split(" ")[1])
        # set batting and pitching lineups
        batters = away_players if top else home_players
        pitchers = home_players if top else away_players
        # play_timing[1]: "num out"
        out = int(play_timing[1].split(" ")[0])
        # play_segments[0]: "[batter] batting against [pitcher]"
        batter = play_segments[0].split(" batting against ")[0]
        pitcher = play_segments[0].split(" batting against ")[1]
        result = play_segments[5]


        # TODO: check names of players moving bases against players that were already on base
        #       - This means players should be some sort of map
        return play_str[0]

    def __init__(self, game_url, away_players, home_players):
        self.team = -1
        self.on1B = -1
        self.on2B = -1
        self.on3B = -1
        self.top = True
        url = "https://baseball-reference.com" + game_url
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        game_data = soup.find_all('script')[12]
        # Find play data
        p = re.search('var chartData = (\[\[(.*)\]\]\;)', game_data.text, re.MULTILINE).group(1)
        p = p.replace("\"", "'")
        p = p.replace("[", "\"[")
        p = p.replace("]", "]\"")
        p_jstr = '{ "plays" : ' + p[1:(len(p) - 2)] + ' }'
        p_json = json.loads(p_jstr)
        playbyplay_data = p_json["plays"]
        self.plays = [None] * len(playbyplay_data)
        for x in range(len(playbyplay_data)):
            play_row = playbyplay_data[x]
            if play_row.find("Start of game") is -1:
                self.plays[x] = (self.create_play(play_row, away_players, home_players))




if __name__ == "__main__":
    scrape = GameScrape("/boxes/SLN/SLN201904080.shtml", [], [])

    #[2, 0.54,
     #"<b>Top 1, 0 out, ---, 1-0 count</b><br>Joc Pederson batting against Miles Mikolas<br>LAD: 0, STL: 0<br>LAD WinExp Start: 50%, End: 54%, Diff: +4%<br>STL WinExp Start: 50%, End: 46%, Diff: -4%<br>Leverage Index: 0.87<br>Hit By Pitch<br>LAD: 0, STL: 0",
     #null, false]