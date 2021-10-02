import unittest

from castledice.common.constants import (
    DeckName,
    MarketCardType,
    PhaseType,
    SpecialPhaseType,
)

from ..exceptions import InvalidMarketCardTypeError
from ..market_cards import (
    Bard,
    HungryBarbarians,
    Jester,
    Maiden,
    MarketCard,
    Shepherd,
    Volunteer,
)
from .utils import CardTestBase


class MarketCardTestBase(CardTestBase):
    deck_name = DeckName.MARKET


class BardTest(MarketCardTestBase):
    card_class = Bard
    card_type = MarketCardType.BARD
    playable_phase_type = SpecialPhaseType.END_GAME

    has_description = True
    has_build_cost = False
    victory_points = 1


class HungryBarbarianTest(MarketCardTestBase):
    card_class = HungryBarbarians
    card_type = MarketCardType.HUNGRY_BARBARIANS
    playable_phase_type = SpecialPhaseType.FIRST_GATHER

    has_description = True


class JesterTest(MarketCardTestBase):
    card_class = Jester
    card_type = MarketCardType.JESTER
    playable_phase_type = PhaseType.GATHER

    has_description = True


class MaidenTest(MarketCardTestBase):
    card_class = Maiden
    card_type = MarketCardType.MAIDEN
    playable_phase_type = PhaseType.GATHER

    has_description = True


class ShepherdTest(MarketCardTestBase):
    card_class = Shepherd
    card_type = MarketCardType.SHEPHERD
    playable_phase_type = SpecialPhaseType.FIRST_GATHER

    has_description = True


class VolunteerTest(MarketCardTestBase):
    card_class = Volunteer
    card_type = MarketCardType.VOLUNTEER
    playable_phase_type = PhaseType.BUILD
    ongoing_phase_type = SpecialPhaseType.ANY

    has_description = True


class VillagerCardTest(unittest.TestCase):
    def test_lookup(self):
        card = MarketCard(MarketCardType.VOLUNTEER)

        self.assertEqual(card.card_id, MarketCardType.VOLUNTEER)

    def test_lookup_error(self):
        with self.assertRaises(InvalidMarketCardTypeError):
            MarketCard("abc")

    def test_all_cards_in_map(self):
        self.assertCountEqual(
            list(MarketCardType.values()), list(MarketCard.card_map.keys())
        )
