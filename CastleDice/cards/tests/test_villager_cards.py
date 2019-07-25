import unittest

from CastleDice.common.constants import DeckName
from CastleDice.common.constants import PhaseType
from CastleDice.common.constants import VillagerCardType
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
    card_type = VillagerCardType.FARMER
    playable_phase_type = PhaseType.BUILD
    has_description = False
    has_build_cost = True


class GuardTest(VillagerCardTestBase):
    card_class = Guard
    card_type = VillagerCardType.GUARD
    playable_phase_type = PhaseType.BUILD
    has_description = False
    has_build_cost = True


class KingsMessengerTest(VillagerCardTestBase):
    card_class = KingsMessenger
    card_type = VillagerCardType.KINGS_MESSENGER
    playable_phase_type = PhaseType.GATHER
    has_build_cost = False
    has_description = True


class MerchantTest(VillagerCardTestBase):
    card_class = Merchant
    card_type = VillagerCardType.MERCHANT
    playable_phase_type = PhaseType.BUILD
    has_build_cost = True
    has_description = False


class SoldierTest(VillagerCardTestBase):
    card_class = Soldier
    card_type = VillagerCardType.SOLDIER
    playable_phase_type = PhaseType.GATHER
    has_build_cost = False
    has_description = True


class WiseGrandfatherTest(VillagerCardTestBase):
    card_class = WiseGrandfather
    card_type = VillagerCardType.WISE_GRANDFATHER
    playable_phase_type = PhaseType.GATHER
    has_build_cost = False
    has_description = True


class WorkerTest(VillagerCardTestBase):
    card_class = Worker
    card_type = VillagerCardType.WORKER
    playable_phase_type = PhaseType.BUILD
    has_description = False
    has_build_cost = True


class VillagerCardTest(unittest.TestCase):
    def test_lookup(self):
        card = VillagerCard(VillagerCardType.MERCHANT)

        self.assertEqual(card.card_id, VillagerCardType.MERCHANT)

    def test_lookup_error(self):
        with self.assertRaises(InvalidVillagerCardTypeError):
            VillagerCard("abc")

    def test_all_cards_in_map(self):
        self.assertCountEqual(
            list(VillagerCardType.values()), list(VillagerCard.card_map.keys())
        )
