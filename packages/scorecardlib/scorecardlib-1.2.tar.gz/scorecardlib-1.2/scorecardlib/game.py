from datetime import datetime


class Game:
    def __init__(self, home_team: str, away_team: str):
        """"Constructor which starts the game with the names of the teams and initializes with 0,0 score"""
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = 0
        self.away_score = 0
        self.start_time = datetime.now()
        self.end_time = None

    def update_score(self, home_score: int, away_score: int):
        """"Method to update the score of an individual match"""
        self.home_score = home_score
        self.away_score = away_score

    def get_scores(self):
        return f"Scores for {self.home_team}-{self.away_team} is {self.home_score}-{self.away_score}"

    def finish_game(self):
        """ Invoking this method will end the game and should be triggered from the scoreboard class ideally """
        self.end_time = datetime.now()

    def total_score(self):
        """This method returns the sum of scores of home and away teams which can be used for scoreboard"""
        return self.home_score + self.away_score

    def __str__(self):
        return f" Match : {self.home_team} {self.home_score} - {self.away_team} {self.away_score}"
