import unittest

from CastleDice.common.constants import ResourceType
from ..turns import FirstTurn
from ..turns import InvalidTurnNumberError
from ..turns import Turn


class TestTurn(unittest.TestCase):
    def test_lookup_succeeds(self):
        first_turn = Turn(1)
        self.assertIsInstance(first_turn, FirstTurn)

        # confirm the method is usable
        self.assertIsInstance(first_turn.create_player_choice_dice_for_turn(), tuple)

    def test_lookup_errors(self):
        for turn_number in [None, 0, 8]:
            with self.assertRaises(InvalidTurnNumberError):
                Turn(turn_number)


class TestTurnMethods(unittest.TestCase):
    def test_creates_choice_dice_list(self):
        expected_dice_bank = (
            [ResourceType.WOOD] * 12
            + [ResourceType.STONE] * 12
            + [ResourceType.GOLD] * 12
            + [ResourceType.LAND] * 11
            + [ResourceType.IRON] * 11
        )
        actual_dice_bank = FirstTurn.create_dice_bank_for_turn()

        self.assertCountEqual(tuple(expected_dice_bank), actual_dice_bank)

    def test_creates_given_dice_list(self):
        expected_given_dice = (
            ResourceType.WOOD,
            ResourceType.WOOD,
            ResourceType.STONE,
            ResourceType.STONE,
            ResourceType.GOLD,
        )

        actual_given_dice = FirstTurn.create_player_choice_dice_for_turn()
        self.assertCountEqual(expected_given_dice, actual_given_dice)
