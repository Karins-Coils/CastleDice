import unittest
from typing import Union

from CastleDice.cards.decks import MarketDeck
from CastleDice.cards.decks import VillagerDeck
from CastleDice.common.constants import CastleCardType
from CastleDice.common.constants import DeckName
from CastleDice.common.constants import MarketCardType
from CastleDice.common.constants import VillagerCardType
from CastleDice.common.tests.utils import create_skip_test_if_base_class_decorator
from ..decks import CastleDeck
from ..decks import _Deck


skip_test_if_base_class = create_skip_test_if_base_class_decorator('deck_class')


class DeckBaseTest(unittest.TestCase):
    deck_class: _Deck = None
    deck_type: DeckName = None
    card_type: Union[CastleCardType, MarketCardType, VillagerCardType] = None

    @skip_test_if_base_class
    def test_attributes(self):
        self.assertEqual(self.deck_class().type, self.deck_type)
        self.assertEqual(self.deck_class._deck_type, self.deck_type)

    @skip_test_if_base_class
    def test_makeup_has_all_cards(self):
        self.assertCountEqual(self.deck_class._deck_makeup.keys(),
                              self.card_type.values())


class _DeckTest(unittest.TestCase):
    def test_all_decks_implemented(self):
        # this dict should be updated whenever a new deck name + class are added
        decks = {
            DeckName.CASTLE: CastleDeck,
            DeckName.MARKET: MarketDeck,
            DeckName.VILLAGER: VillagerDeck,
        }

        self.assertCountEqual(decks.keys(), DeckName.values())


class CastleDeckTest(DeckBaseTest):
    deck_class = CastleDeck
    deck_type = DeckName.CASTLE
    card_type = CastleCardType


class MarketDeckTest(DeckBaseTest):
    deck_class = MarketDeck
    deck_type = DeckName.MARKET
    card_type = MarketCardType


class VillagerDeckTest(DeckBaseTest):
    deck_class = VillagerDeck
    deck_type = DeckName.VILLAGER
    card_type = VillagerCardType
