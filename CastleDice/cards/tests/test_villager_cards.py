import unittest

from CastleDice.common import DeckName
from CastleDice.common import PhaseType
from CastleDice.common import VillagerCardType
from .utils import CardTestBase
from ..exceptions import InvalidVillagerCardTypeError
from ..villager_cards import Farmer
from ..villager_cards import Guard
from ..villager_cards import KingsMessenger
from ..villager_cards import Merchant
from ..villager_cards import Soldier
from ..villager_cards import VillagerCard
from ..villager_cards import WiseGrandfather
from ..villager_cards import Worker


class VillagerCardTestBase(CardTestBase):
    deck_name = DeckName.VILLAGER


class FarmerTest(VillagerCardTestBase):
    card_class = Farmer
    playable_phase_type = PhaseType.BUILD
    has_description = False
    has_build_cost = True


class GuardTest(VillagerCardTestBase):
    card_class = Guard
    playable_phase_type = PhaseType.BUILD
    has_description = False
    has_build_cost = True


class KingsMessengerTest(VillagerCardTestBase):
    card_class = KingsMessenger
    playable_phase_type = PhaseType.GATHER
    has_build_cost = False
    has_description = True


class MerchantTest(VillagerCardTestBase):
    card_class = Merchant
    playable_phase_type = PhaseType.BUILD
    has_build_cost = True
    has_description = False


class SoldierTest(VillagerCardTestBase):
    card_class = Soldier
    playable_phase_type = PhaseType.GATHER
    has_build_cost = False
    has_description = True


class WiseGrandfatherTest(VillagerCardTestBase):
    card_class = WiseGrandfather
    playable_phase_type = PhaseType.GATHER
    has_build_cost = False
    has_description = True


class WorkerTest(VillagerCardTestBase):
    card_class = Worker
    playable_phase_type = PhaseType.BUILD
    has_description = False
    has_build_cost = True


class VillagerCardTest(unittest.TestCase):
    def test_lookup(self):
        card = VillagerCard(VillagerCardType.MERCHANT)

        self.assertEqual(card.card_id, VillagerCardType.MERCHANT)

    def test_lookup_error(self):
        with self.assertRaises(InvalidVillagerCardTypeError):
            VillagerCard('abc')
