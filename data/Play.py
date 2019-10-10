
class Play:

    def __init__(self, top, inning, out, batter, play_on1b, play_on2b, play_on3b, result, play_1b_finished, play_2b_finished, play_3b_finished):
        self.top = top
        self.inning = inning
        self.out = out
        self.batter = batter
        self.on1B = play_on1b
        self.on2B = play_on2b
        self.on3B = play_on3b
        self.result = result
        self.finishedFrom1B = play_1b_finished
        self.finishedFrom2B = play_2b_finished
        self.finishedFrom3B = play_3b_finished

    def scored_from1b(self):
        return self.finishedFrom1B == 4

    def scored_from2b(self):
        return self.finishedFrom2B == 4

    def scored_from3b(self):
        return self.finishedFrom3B == 4
