import unittest

from gamebuilder import PlayerSpecification
from gamebuilder import BayesianGame


class SampleGame(BayesianGame):

    def __init__(self):
        super(SampleGame, self).__init__(
            player_specification=PlayerSpecification(player_types=[1, 2], player_actions=["U", "D"]),
            opponent_specification=PlayerSpecification(player_types=[1, 2],
                                                       player_actions=["R",
                                                                       "L"]))

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

    def get_types_probability(self, player_type, opponent_type):
        return self.type_probability[(player_type, opponent_type)]

    def get_utility(self, player_type, player_strategy, opponent_type, opponent_strategy):
        player_index = player_type - 1
        player_action = player_strategy[player_index]

        opponent_index = opponent_type - 1
        opponent_action = opponent_strategy[opponent_index]

        return self.utility_values[(player_type, player_action, opponent_type, opponent_action)]


class PlayerSpecificationTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(PlayerSpecificationTest, self).__init__(*args, **kwargs)
        self.sample_game = SampleGame()

    def test_pure_strategies(self):
        expected_strategies = {("U", "U"), ("U", "D"), ("D", "U"), ("D", "D")}
        actual_strategies = get_all_strategies(self.sample_game.player_specification)

        self.assertEqual(actual_strategies, expected_strategies)

        expected_strategies = {("R", "R"), ("R", "L"), ("L", "R"), ("L", "L")}
        actual_strategies = get_all_strategies(self.sample_game.opponent_specification)
        self.assertEqual(actual_strategies, expected_strategies)

    def test_get_utility(self):
        expected_opponent_utility = 1.
        player_strategy = ("U", "U")
        opponent_strategy = ("L", "L")
        actual_player_utility, actual_opponent_utility = self.sample_game.get_expected_utilities(
            (player_strategy, opponent_strategy))

        self.assertAlmostEqual(actual_opponent_utility, expected_opponent_utility)


def get_all_strategies(player_specification):
    actual_strategies = set()
    for pure_strategy in player_specification.get_pure_strategies():
        actual_strategies.add(pure_strategy)

    return actual_strategies
