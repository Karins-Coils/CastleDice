import unittest


from CastleDice.common.constants import CastleCardType
from CastleDice.common.constants import DeckName
from CastleDice.common.constants import MarketCardType
from CastleDice.common .constants import VillagerCardType
from ..castle_cards import CastleCard
from ..exceptions import InvalidDeckCardTypeError
from ..market_cards import MarketCard
from ..utils import DeckCard
from ..villager_cards import VillagerCard


class DeckCardTest(unittest.TestCase):
    def test_unknown_card_errors(self):
        with self.assertRaises(InvalidDeckCardTypeError):
            DeckCard('abcd')

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
