

class Play:
    def __init__(self, game_id, play_id, batter_id, pitcher_id, home, balls, strikes,
                 on_1b, on_2b, on_3b, result, finished_h, finished_1b, finished_2b, finished_3b):
        self.game_id = game_id
        self.batter_id = batter_id
        self.pitcher_id = pitcher_id
        self.home = home
        self.balls = balls
        self.strikes = strikes
        self.on_1B = on_1b
        self.on_2B = on_2b
        self.on_3B = on_3b
        self.result = result
        self.finished_H = finished_h
        self.finished_1B = finished_1b
        self.finished_2B = finished_2b
        self.finished_3B = finished_3b
        self.play_id = play_id
