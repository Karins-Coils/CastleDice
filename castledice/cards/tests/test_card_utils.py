import unittest

from castledice.common.constants import (
    CastleCardType,
    DeckName,
    MarketCardType,
    VillagerCardType,
)

from ..exceptions import InvalidDeckCardTypeError
from ..utils import DeckCard


class DeckCardTest(unittest.TestCase):
    def test_unknown_card_errors(self):
        with self.assertRaises(InvalidDeckCardTypeError):
            DeckCard("abcd")

    def test_gets_castle_card(self):
        card = DeckCard(CastleCardType.SQUIRE)

        self.assertEqual(card.card_id, CastleCardType.SQUIRE.value)
        self.assertEqual(card.deck_type, DeckName.CASTLE)

    def test_gets_market_card(self):
        card = DeckCard(MarketCardType.BARD)

        self.assertEqual(card.card_id, MarketCardType.BARD.value)
        self.assertEqual(card.deck_type, DeckName.MARKET)

    def test_gets_villager_card(self):
        card = DeckCard(VillagerCardType.GUARD)

        self.assertEqual(card.card_id, VillagerCardType.GUARD.value)
        self.assertEqual(card.deck_type, DeckName.VILLAGER)
