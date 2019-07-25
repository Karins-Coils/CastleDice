import unittest
from typing import ClassVar
from typing import Union
from typing import Type

from CastleDice.cards.castle_cards import CastleCard
from CastleDice.cards.decks import MarketDeck
from CastleDice.cards.decks import VillagerDeck
from CastleDice.cards.villager_cards import VillagerCard
from CastleDice.common.constants import CastleCardType
from CastleDice.common.constants import DeckName
from CastleDice.common.constants import MarketCardType
from CastleDice.common.constants import VillagerCardType
from CastleDice.common.tests.utils import create_skip_test_if_base_class_decorator
from ..decks import CastleDeck
from ..decks import _Deck


skip_test_if_base_class = create_skip_test_if_base_class_decorator("deck_class")


class DeckBaseTest(unittest.TestCase):
    deck_class: ClassVar[Type[_Deck]] = None
    deck_type: ClassVar[DeckName] = None
    card_type: ClassVar[Union[CastleCardType, MarketCardType, VillagerCardType]] = None

    @skip_test_if_base_class
    def test_attributes(self):
        self.assertEqual(self.deck_class().type, self.deck_type)
        self.assertEqual(self.deck_class._deck_type, self.deck_type)
        self.assertEqual(self.deck_class._card_type, self.card_type)
        self.assertIsNotNone(self.deck_class._card_type_error)

    @skip_test_if_base_class
    def test_makeup_has_all_cards(self):
        self.assertCountEqual(
            self.deck_class._deck_makeup.keys(), self.card_type.values()
        )

    @skip_test_if_base_class
    def test_create_draw_pile(self):
        total_cards = sum(self.deck_class._deck_makeup.values())
        deck = self.deck_class()
        deck.create_and_shuffle_draw_pile()
        self.assertEqual(len(deck._draw_pile), total_cards)


class _DeckTest(unittest.TestCase):
    def test_all_decks_implemented(self):
        # this dict should be updated whenever a new deck name + class are added
        decks = {
            DeckName.CASTLE: CastleDeck,
            DeckName.MARKET: MarketDeck,
            DeckName.VILLAGER: VillagerDeck,
        }

        self.assertCountEqual(decks.keys(), DeckName.values())

    def test_initialized_empty(self):
        deck = _Deck()
        self.assertEqual(deck._discard_pile, [])
        self.assertEqual(deck._draw_pile, [])


class CastleDeckTest(DeckBaseTest):
    deck_class = CastleDeck
    deck_type = DeckName.CASTLE
    card_type = CastleCardType

    # -- These tests are testing base functionality,
    # -- but are easier when a deck has been properly set
    def test_initialized_with_piles(self):
        draw_pile = [
            CastleCard(CastleCardType.ADVISOR),
            CastleCard(CastleCardType.SQUIRE),
        ]
        discard_pile = [
            CastleCard(CastleCardType.DEEP_MOAT),
            CastleCard(CastleCardType.DAUGHTER),
        ]
        deck = CastleDeck(draw_pile, discard_pile)
        self.assertEqual(deck._draw_pile, draw_pile)
        self.assertEqual(deck._discard_pile, discard_pile)

        # modify the local lists, confirming that the class instance lists aren't affected
        draw_pile.pop()
        discard_pile.pop()
        self.assertNotEqual(deck._draw_pile, draw_pile)
        self.assertNotEqual(deck._discard_pile, discard_pile)

    def test_initialized_with_bad_draw_pile(self):
        draw_pile = [
            VillagerCard(VillagerCardType.WORKER),
            CastleCard(CastleCardType.SQUIRE),
        ]
        discard_pile = []
        with self.assertRaises(CastleDeck._card_type_error):
            CastleDeck(draw_pile, discard_pile)

    def test_initialized_with_bad_discard_pile(self):
        draw_pile = []
        discard_pile = [
            VillagerCard(VillagerCardType.WORKER),
            CastleCard(CastleCardType.SQUIRE),
        ]
        with self.assertRaises(CastleDeck._card_type_error):
            CastleDeck(draw_pile, discard_pile)

    def test_shuffle_draw_cards(self):
        draw_pile = [
            CastleCard(CastleCardType.ADVISOR),
            CastleCard(CastleCardType.SQUIRE),
        ]
        discard_pile = [
            CastleCard(CastleCardType.DEEP_MOAT),
            CastleCard(CastleCardType.DAUGHTER),
            CastleCard(CastleCardType.DAUGHTER),
            CastleCard(CastleCardType.GREAT_HALL),
            CastleCard(CastleCardType.GATE_HOUSE),
            CastleCard(CastleCardType.GREAT_HALL),
        ]
        deck = CastleDeck(draw_pile, discard_pile)
        deck.shuffle_draw_cards()
        self.assertEqual(len(draw_pile), len(deck._draw_pile))

    def test_shuffle_discard_pile(self):
        draw_pile = [
            CastleCard(CastleCardType.ADVISOR),
            CastleCard(CastleCardType.SQUIRE),
        ]
        discard_pile = [
            CastleCard(CastleCardType.DEEP_MOAT),
            CastleCard(CastleCardType.DAUGHTER),
            CastleCard(CastleCardType.DAUGHTER),
            CastleCard(CastleCardType.GREAT_HALL),
            CastleCard(CastleCardType.GATE_HOUSE),
            CastleCard(CastleCardType.GREAT_HALL),
        ]
        deck = CastleDeck(draw_pile, discard_pile)
        deck.shuffle_discard_cards()
        self.assertEqual(len(discard_pile), len(deck._discard_pile))

    def test_reshuffle_discard_into_draw_pile(self):
        draw_pile = [
            CastleCard(CastleCardType.ADVISOR),
            CastleCard(CastleCardType.SQUIRE),
        ]
        discard_pile = [
            CastleCard(CastleCardType.DEEP_MOAT),
            CastleCard(CastleCardType.DAUGHTER),
            CastleCard(CastleCardType.DAUGHTER),
            CastleCard(CastleCardType.GREAT_HALL),
            CastleCard(CastleCardType.GATE_HOUSE),
            CastleCard(CastleCardType.GREAT_HALL),
        ]
        deck = CastleDeck(draw_pile, discard_pile)
        deck.reshuffle_discard_into_draw()
        self.assertEqual(deck._discard_pile, [])
        self.assertEqual(len(deck._draw_pile), len(draw_pile) + len(discard_pile))

        # first two cards should be on top, always
        self.assertListEqual(deck._draw_pile[0:2], draw_pile)

    def test_serialize_draw_pile(self):
        draw_pile = [
            CastleCard(CastleCardType.ADVISOR),
            CastleCard(CastleCardType.SQUIRE),
        ]
        discard_pile = []
        deck = CastleDeck(draw_pile, discard_pile)

        self.assertEqual(
            deck.serialize_draw_pile(),
            [CastleCardType.ADVISOR.value, CastleCardType.SQUIRE.value],
        )

    def test_serialize_discard_pile(self):
        draw_pile = []
        discard_pile = [
            CastleCard(CastleCardType.DEEP_MOAT),
            CastleCard(CastleCardType.DAUGHTER),
        ]
        deck = CastleDeck(draw_pile, discard_pile)

        self.assertEqual(
            deck.serialize_discard_pile(),
            [CastleCardType.DEEP_MOAT.value, CastleCardType.DAUGHTER.value],
        )

    def test_serialize_empty_deck(self):
        deck = CastleDeck([], [])
        self.assertEqual(deck.serialize_draw_pile(), [])
        self.assertEqual(deck.serialize_discard_pile(), [])


class MarketDeckTest(DeckBaseTest):
    deck_class = MarketDeck
    deck_type = DeckName.MARKET
    card_type = MarketCardType


class VillagerDeckTest(DeckBaseTest):
    deck_class = VillagerDeck
    deck_type = DeckName.VILLAGER
    card_type = VillagerCardType
