import requests
from bs4 import BeautifulSoup


class TeamScheduleScrape:
    def __init__(self, team, year):
        self.games = []
        url = 'https://www.baseball-reference.com/teams/' + team + '/' + str(year) + '-schedule-scores.shtml'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        games_data = soup.find(id='timeline_results').findAll('li')
        for row in games_data:
            if row['class'][0] == "result":
                game_url = row.find('a')['href']
                self.games.append(game_url)


if __name__ == "__main__":
    teams = ['BAL', 'BOS', 'NYY', 'TBR', 'TOR',
             'ATL', 'MIA', 'NYM', 'PHI', 'WSN',
             'CHW', 'CLE', 'DET', 'KCR', 'MIN',
             'CHC', 'CIN', 'MIL', 'PIT', 'STL',
             'HOU', 'LAA', 'OAK', 'SEA', 'TEX',
             'ARI', 'COL', 'LAD', 'SDP', 'SFG']
    scrape = TeamScheduleScrape(teams[19], 2019)
    numGames = len(scrape.games)
    success = numGames == 162
    if success:
        print("Nailed it")
    else:
        print("Needs work, actually found " + str(numGames))

