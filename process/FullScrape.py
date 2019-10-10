from scrape import GameScrape, RosterScrape, TeamScheduleScrape
from consts import teams

if __name__ == "__main__":
    for t in teams:
        roster = RosterScrape(t, 2019)

