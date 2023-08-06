from scorecardlib.game import Game
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Scoreboard:
    games: Dict[str, Game] = field(default_factory=dict)

    def start_game(self, home_team: str, away_team: str):
        """Calling this method with team names will add this as
        a key as joins of names and game  instance as value"""
        game = Game(home_team, away_team)
        if f"{home_team}-{away_team}" in self.games.keys():
            raise Exception(f"There is an ongoing game between {home_team} and {away_team}\n")
        else:
            self.games[f"{home_team}-{away_team}"] = game

    def check_if_match_ongoing(self, home_team, away_team):
        """This takes care of the edge cases where the score update is failed if a match does not exist"""
        if f"{home_team}-{away_team}" not in self.games.keys():
            # validate if the given combination of teams exist in scoreboard
            raise Exception(f"There is no ongoing game between {home_team} and {away_team}\n")
        return True

    def update_score(self, home_team: str, away_team: str, home_score: int, away_score: int):
        """this method updates the score of any running games in scoreboard"""
        match_key = f"{home_team}-{away_team}"
        if self.check_if_match_ongoing(home_team, away_team):
            self.games[match_key].home_score = home_score
            self.games[match_key].away_score = away_score

    def get_game_score(self, home_team, away_team):
        match_key = f"{home_team}-{away_team}"
        if self.check_if_match_ongoing(home_team, away_team):
            return self.games[match_key].get_scores()

    def finish_game(self, home_team, away_team):
        if self.check_if_match_ongoing(home_team, away_team):
            match_key = f"{home_team}-{away_team}"
            self.games[match_key].finish_game()
            # finishing a game from leaderboard will trigger  finish_game of the Game class
            self.games.pop(match_key)

    def get_games_summary(self, verbose=True):
        sorted_games = sorted(self.games.values(), key=lambda x: (x.total_score(), x.start_time), reverse=True)
        if verbose:
            for game in sorted_games:
                print(game)
        return sorted_games
