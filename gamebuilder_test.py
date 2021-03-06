import unittest

from gamebuilder import PlayerSpecification
from gamebuilder import BayesianGame


class SampleGame(BayesianGame):
    """
    This is the sample bayesian game contained in Chapter 7 of Essentials of Game Theory by Leyton-Brown.
    """

    def __init__(self):
        player_specification = PlayerSpecification(player_types=[1, 2], player_actions=["U", "D"])
        opponent_specification = PlayerSpecification(player_types=[1, 2],
                                                     player_actions=["R",
                                                                     "L"])

        super(SampleGame, self).__init__(
            game_name="Sample_Game",
            player_specifications=[player_specification, opponent_specification])

        self.type_probability = {(1, 1): .3,
                                 (1, 2): .1,
                                 (2, 1): .2,
                                 (2, 2): .4}

        self.utility_values = {(1, "U", 1, "L"): (2, 0),
                               (1, "U", 2, "L"): (2, 2),
                               (2, "U", 1, "L"): (2, 2),
                               (2, "U", 2, "L"): (2, 1),
                               (1, "U", 1, "R"): (0, 2),
                               (1, "U", 2, "R"): (0, 3),
                               (2, "U", 1, "R"): (0, 0),
                               (2, "U", 2, "R"): (0, 0),
                               (1, "D", 1, "L"): (0, 2),
                               (1, "D", 2, "L"): (3, 0),
                               (2, "D", 1, "L"): (0, 0),
                               (2, "D", 2, "L"): (0, 0),
                               (1, "D", 1, "R"): (2, 0),
                               (1, "D", 2, "R"): (1, 1),
                               (2, "D", 1, "R"): (1, 1),
                               (2, "D", 2, "R"): (1, 2)}

    def get_types_probability(self, player_types):
        return self.type_probability[player_types]

    def get_utility(self, player_types, strategy_profile):
        player_type, opponent_type = player_types
        player_strategy, opponent_strategy = strategy_profile

        player_type_index = self.player_specifications[0].get_type_index(player_type)
        player_action = player_strategy[player_type_index]

        opponent_type_index = self.player_specifications[1].get_type_index(opponent_type)
        opponent_action = opponent_strategy[opponent_type_index]

        return self.utility_values[(player_type, player_action, opponent_type, opponent_action)]


class BayesianGameTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(BayesianGameTest, self).__init__(*args, **kwargs)
        self.sample_game = SampleGame()

        self.player_specification = self.sample_game.player_specifications[0]
        self.opponent_specification = self.sample_game.player_specifications[1]

    def test_pure_strategies(self):
        expected_strategies = [("U", "U"), ("U", "D"), ("D", "U"), ("D", "D")]
        actual_strategies = list(self.player_specification.get_pure_strategies())

        self.assertEqual(actual_strategies, expected_strategies)

        expected_strategies = [("R", "R"), ("R", "L"), ("L", "R"), ("L", "L")]
        actual_strategies = list(self.opponent_specification.get_pure_strategies())
        self.assertEqual(actual_strategies, expected_strategies)

    def test_get_utility(self):
        expected_player_utility = 2.
        expected_opponent_utility = 1.
        player_strategy = ("U", "U")
        opponent_strategy = ("L", "L")

        actual_player_utility, actual_opponent_utility = self.sample_game.get_expected_utilities(
            (player_strategy, opponent_strategy))
        self.assertAlmostEqual(actual_player_utility, expected_player_utility)
        self.assertAlmostEqual(actual_opponent_utility, expected_opponent_utility)

        expected_player_utility = 0.7
        expected_opponent_utility = 0.1
        player_strategy = ("D", "U")
        opponent_strategy = ("R", "R")

        actual_player_utility, actual_opponent_utility = self.sample_game.get_expected_utilities(
            (player_strategy, opponent_strategy))
        self.assertAlmostEqual(actual_player_utility, expected_player_utility)
        self.assertAlmostEqual(actual_opponent_utility, expected_opponent_utility)

    def test_to_nfg_file(self):
        nfg_file, _ = self.sample_game.to_nfg_file()
        expected_file_name = self.sample_game.game_name + ".nfg"
        self.assertEqual(nfg_file, expected_file_name)
