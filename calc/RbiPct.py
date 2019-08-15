

class RbiPct:
    def __init__(self, player):
        total_on1b = 0
        total_on2b = 0
        total_on3b = 0
        total_scored_from1b = 0
        total_scored_from2b = 0
        total_scored_from3b = 0
        for p in player.plays:
            if p.on1B > 0:
                total_on1b += 1
            if p.on2B > 0:
                total_on2b += 1
            if p.on3B > 0:
                total_on3b += 1
            if p.scoredFrom1B():
                total_scored_from1b += 1
            if p.scoredFrom2B():
                total_scored_from2b += 1
            if p.scored_from3B():
                total_scored_from3b += 1

        self.pct1B = total_scored_from1b / total_on1b
        self.pct2B = total_scored_from2b / total_on2b
        self.pct3B = total_scored_from3b / total_on3b
