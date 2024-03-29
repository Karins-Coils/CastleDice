import unittest
from typing import List, Optional, Union

from castledice.common.constants import PhaseType
from castledice.common.tests.utils import (
    create_skip_if_not_implemented_decorator,
    create_skip_test_if_base_class_decorator,
)

from ..castle_cards import CastleCard
from ..market_cards import MarketCard
from ..villager_cards import VillagerCard

__all__ = ["CardTestBase"]


skip_test_if_base_class = create_skip_test_if_base_class_decorator("card_class")
skip_if_not_implemented = create_skip_if_not_implemented_decorator("card")


def serialize_pile(
    pile: Optional[Union[List[Union[CastleCard, MarketCard, VillagerCard]], List[str]]],
) -> List[str]:
    serialized = []
    for card in pile:
        if isinstance(card, str):
            serialized.append(card)
            continue
        serialized.append(getattr(card, "card_id"))
    return serialized


class CardTestBase(unittest.TestCase):
    card_class = None
    card_type = None
    deck_name = None
    playable_phase_type = None
    ongoing_phase_type = None
    has_description = False
    has_build_cost = False
    victory_points = 0

    def setUp(self):
        self.card = None
        if self.card_class:
            self.card = self.card_class()

    # -- helper functions -- #

    # -- Test card props -- #
    @skip_test_if_base_class
    def test_base_properties(self):
        self.assertTrue(self.card)
        self.assertEqual(self.card.card_id, self.card_type.value)
        self.assertTrue(self.card.name)

    @skip_test_if_base_class
    def test_description(self):
        if self.has_description:
            self.assertIsNotNone(self.card.description)
        else:
            self.assertIsNone(self.card.description)

    @skip_test_if_base_class
    def test_playable_phase(self):
        self.assertEqual(self.card.playable_phase, self.playable_phase_type)

    @skip_test_if_base_class
    def test_ongoing_phase(self):
        self.assertEqual(self.card.ongoing_phase, self.ongoing_phase_type)

    @skip_test_if_base_class
    def test_deck_type(self):
        self.assertEqual(self.card.deck_type, self.deck_name)

    @skip_test_if_base_class
    def test_victory_points(self):
        self.assertEqual(self.card.victory_points, self.victory_points)

    @skip_test_if_base_class
    def test_build_cost(self):
        if self.has_build_cost:
            self.assertTrue(len(self.card.build_cost))
            self.assertEqual(self.card.playable_phase, PhaseType.BUILD)
        else:
            self.assertEqual(self.card.build_cost, ())

    # -- Test card functions -- #
    @skip_test_if_base_class
    def test_serialize(self):
        self.assertEqual(self.card.serialize(), self.card.card_id)

    @skip_test_if_base_class
    @skip_if_not_implemented("is_playable")
    def test_is_playable(self):
        self.fail("Must implement this feature and its test")

    @skip_test_if_base_class
    @skip_if_not_implemented("play")
    def test_play(self):
        self.fail("Must implement this feature and its test")

    @skip_test_if_base_class
    @skip_if_not_implemented("score")
    def test_score(self):
        if self.victory_points > 0:
            self.fail("Must implement this feature and its test")

    @skip_test_if_base_class
    @skip_if_not_implemented("discard")
    def test_discard(self):
        self.fail("Must implement this feature and its test")

    @skip_test_if_base_class
    @skip_if_not_implemented("use_ongoing")
    def test_use_ongoing(self):
        self.fail("Must implement this feature and its test")

    @skip_test_if_base_class
    @skip_if_not_implemented("has_ongoing_choice")
    def test_has_ongoing_choice(self):
        self.fail("Must implement this feature and its test")

    @skip_test_if_base_class
    @skip_if_not_implemented("can_use_ongoing")
    def test_can_use_ongoing(self):
        self.fail("Must implement this feature and its test")

    @skip_test_if_base_class
    @skip_if_not_implemented("reset_ongoing")
    def test_reset_ongoing(self):
        self.fail("Must implement this feature and its test")
