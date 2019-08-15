import requests
from bs4 import BeautifulSoup


class TeamScheduleScrape:
    def __init__(self, year):
        teams = ['BAL', 'BOS', 'NYY', 'TBR', 'TOR',
                 'ATL', 'MIA', 'NYM', 'PHI', 'WSN',
                 'CHW', 'CLE', 'DET', 'KCR', 'MIN',
                 'CHC', 'CIN', 'MIL', 'PIT', 'STL',
                 'HOU', 'LAA', 'OAK', 'SEA', 'TEX',
                 'ARI', 'COL', 'LAD', 'SDP', 'SFG']
        for team in teams:
            url = 'https://www.baseball-reference.com/teams/' + team + '/' + str(year) + '-schedule-scores.shtml'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            games = soup.find(id='timeline_results')


if __name__ == "__main__":
    scrape = TeamScheduleScrape(2019)

