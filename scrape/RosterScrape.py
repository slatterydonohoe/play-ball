import requests
from bs4 import BeautifulSoup


class RosterScrape:
    def __init__(self, team, year):
        self.roster = []
        url = 'https://www.baseball-reference.com/teams/' + team + '/' + str(year) + '-roster.shtml'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        roster_data = soup.find(id='appearances').find('tbody').findAll('tr')
        for row in roster_data:
            name = row.find('th')['csk']
            self.roster.append(name)


if __name__ == "__main__":
    teams = ['BAL', 'BOS', 'NYY', 'TBR', 'TOR',
             'ATL', 'MIA', 'NYM', 'PHI', 'WSN',
             'CHW', 'CLE', 'DET', 'KCR', 'MIN',
             'CHC', 'CIN', 'MIL', 'PIT', 'STL',
             'HOU', 'LAA', 'OAK', 'SEA', 'TEX',
             'ARI', 'COL', 'LAD', 'SDP', 'SFG']
    scrape = RosterScrape(teams[19], 2019)
    success = len(scrape.roster) == 41
    if success:
        print("Nailed it")
    else:
        print("Needs work")

