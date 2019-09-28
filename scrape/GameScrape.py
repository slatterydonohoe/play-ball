import requests
from bs4 import BeautifulSoup
import re
import ast
import json


class GameScrape:
    def __init__(self, game_url):
        url = "https://baseball-reference.com" + game_url
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        game_data = soup.find_all('script')[12]
        p = re.search('var chartData = (\[\[(.*)\]\]\;)', game_data.text, re.MULTILINE).group(1)
        p = p.replace("\"", "'")
        p = p.replace("[", "\"[")
        p = p.replace("]", "]\"")
        p_jstr = '{ "plays" : ' + p[1:(len(p) - 2)] + ' }'
        #
        p_json = json.loads(p_jstr)
        playbyplay_data = p_json["plays"]


if __name__ == "__main__":
    scrape = GameScrape("/boxes/SLN/SLN201904080.shtml")