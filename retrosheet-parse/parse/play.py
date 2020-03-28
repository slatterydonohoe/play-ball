

class Play:
    def __init__(self, game_id, batter_id, pitcher_id, balls, strikes,
                 on_1B, on_2B, on_3B, result, finished_H, finished_1B, finished_2B, finished_3B):
        self.game_id = game_id
        self.batter_id = batter_id
        self.pitcher_id = pitcher_id
        self.balls = balls
        self.strikes = strikes
        self.on_1B = on_1B
        self.on_2B = on_2B
        self.on_3B = on_3B
        self.result = result
        self.finished_H = finished_H
        self.finished_1B = finished_1B
        self.finished_2B = finished_2B
        self.finished_3B = finished_3B
