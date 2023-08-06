from unittest import TestCase
from scorecardlib.game import Game
"""Sample table provided as an input and can be used for writing tests as well"""

# a. Mexico 0 - Canada 5
# b. Spain 10 - Brazil 2
# c. Germany 2 - France 2
# d. Uruguay 6 - Italy 6
# e. Argentina 3 - Australia 1


class TestGame(TestCase):
    def test_game_init(self):
        game = Game(home_team="Mexico", away_team="Canada")
        self.assertEqual(game.home_team, "Mexico")
        self.assertEqual(game.away_team, "Canada")
        self.assertEqual(game.home_score, 0)
        self.assertEqual(game.away_score, 0)
        self.assertIsNotNone(game.start_time)
        self.assertIsNone(game.end_time)

    def test_update_score(self):
        game = Game(home_team="Mexico", away_team="Canada")
        game.update_score(home_score=0, away_score=5)
        self.assertEqual(game.home_team, "Mexico")
        self.assertEqual(game.away_team, "Canada")
        self.assertEqual(game.home_score, 0)
        self.assertEqual(game.away_score, 5)
        self.assertIsNotNone(game.start_time)
        self.assertIsNone(game.end_time)

    def test_finish_game(self):
        game = Game(home_team="Mexico", away_team="Canada")
        game.update_score(home_score=0, away_score=10)
        self.assertEqual(game.home_team, "Mexico")
        self.assertEqual(game.away_team, "Canada")
        self.assertEqual(game.home_score, 0)
        self.assertEqual(game.away_score, 10)
        game.finish_game()
        self.assertIsNotNone(game.start_time)
        self.assertIsNotNone(game.end_time)

    def test_total_score(self):
        game = Game(home_team="Mexico", away_team="Canada")
        game.update_score(home_score=5, away_score=10)
        self.assertEqual(game.home_team, "Mexico")
        self.assertEqual(game.away_team, "Canada")
        self.assertEqual(game.home_score, 5)
        self.assertEqual(game.away_score, 10)
        self.assertEqual(game.total_score(), 15)

        del game

        game = Game(home_team="Spain", away_team="Brazil")
        game.update_score(home_score=10, away_score=2)
        self.assertEqual(game.home_team, "Spain")
        self.assertEqual(game.away_team, "Brazil")
        self.assertEqual(game.home_score, 10)
        self.assertEqual(game.away_score, 2)
        self.assertEqual(game.total_score(), 12)

    def test_get_score(self):
        game = Game(home_team="Spain", away_team="Brazil")
        game.update_score(home_score=10, away_score=2)
        response = f"Scores for Spain-Brazil is 10-2"
        self.assertEqual(game.get_scores(), response)
