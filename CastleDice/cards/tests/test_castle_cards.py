import unittest

from CastleDice.cards.exceptions import InvalidVillagerCardTypeError
from CastleDice.common import CastleCardType
from CastleDice.common import DeckName
from CastleDice.common import PhaseType
from CastleDice.common import SpecialPhaseType
from .utils import CardTestBase
from ..castle_cards import Advisor
from ..castle_cards import Alchemist
from ..castle_cards import CastleCard
from ..castle_cards import Daughter
from ..castle_cards import DeepMoat
from ..castle_cards import GateHouse
from ..castle_cards import GreatHall
from ..castle_cards import LoyalBrother
from ..castle_cards import RoyalChambers
from ..castle_cards import Squire
from ..castle_cards import StrongTower
from ..castle_cards import TallKeep
from ..castle_cards import WallAnimal
from ..castle_cards import WallFarmer
from ..castle_cards import WallGuard
from ..castle_cards import WallMerchant
from ..castle_cards import WallWorker
from ..exceptions import InvalidCastleCardTypeError


class CastleCardTestBase(CardTestBase):
    deck_name = DeckName.CASTLE


class AdvisorTest(CastleCardTestBase):
    card_class = Advisor
    card_type = CastleCardType.ADVISOR
    playable_phase_type = SpecialPhaseType.FIRST_GATHER
    has_description = True


class AlchemistTest(CastleCardTestBase):
    card_class = Alchemist
    card_type = CastleCardType.ALCHEMIST
    playable_phase_type = PhaseType.BUILD
    has_description = True


class DaughterTest(CastleCardTestBase):
    card_class = Daughter
    card_type = CastleCardType.DAUGHTER
    playable_phase_type = PhaseType.GATHER
    has_description = True


class DeepMoatTest(CastleCardTestBase):
    card_class = DeepMoat
    card_type = CastleCardType.DEEP_MOAT
    playable_phase_type = PhaseType.BUILD
    ongoing_phase_type = PhaseType.GATHER
    victory_points = 2
    has_build_cost = True
    has_description = True


class GateHouseTest(CastleCardTestBase):
    card_class = GateHouse
    card_type = CastleCardType.GATE_HOUSE
    playable_phase_type = PhaseType.BUILD
    has_build_cost = True
    victory_points = 2


class GreatHallTest(CastleCardTestBase):
    card_class = GreatHall
    card_type = CastleCardType.GREAT_HALL
    playable_phase_type = PhaseType.BUILD
    has_build_cost = True
    victory_points = 3


class LoyalBrotherTest(CastleCardTestBase):
    card_class = LoyalBrother
    card_type = CastleCardType.LOYAL_BROTHER
    playable_phase_type = PhaseType.CHOOSE
    has_description = True


class RoyalChambersTest(CastleCardTestBase):
    card_class = RoyalChambers
    card_type = CastleCardType.ROYAL_CHAMBERS
    playable_phase_type = PhaseType.BUILD
    has_build_cost = True
    has_description = True
    victory_points = 1
    ongoing_phase_type = PhaseType.CHOOSE


class SquireTest(CastleCardTestBase):
    card_class = Squire
    card_type = CastleCardType.SQUIRE
    playable_phase_type = PhaseType.GATHER
    has_description = True


class StrongTowerTest(CastleCardTestBase):
    card_class = StrongTower
    card_type = CastleCardType.STRONG_TOWER
    playable_phase_type = PhaseType.BUILD
    has_build_cost = True
    has_description = True
    victory_points = 3


class TallKeepTest(CastleCardTestBase):
    card_class = TallKeep
    card_type = CastleCardType.TALL_KEEP
    playable_phase_type = PhaseType.BUILD
    has_build_cost = True
    has_description = True
    victory_points = 4


class WallAnimalTest(CastleCardTestBase):
    card_class = WallAnimal
    card_type = CastleCardType.WALL_ANIMAL
    playable_phase_type = PhaseType.BUILD
    has_build_cost = True
    has_description = True
    victory_points = 0

    @unittest.skip("Logic has not been implemented yet, but should be")
    def test_has_animal_stored_on_card(self):
        pass


class WallFarmerTest(CastleCardTestBase):
    card_class = WallFarmer
    card_type = CastleCardType.WALL_FARMER
    playable_phase_type = PhaseType.BUILD
    has_build_cost = True
    has_description = True
    victory_points = 0


class WallGuardTest(CastleCardTestBase):
    card_class = WallGuard
    card_type = CastleCardType.WALL_GUARD
    playable_phase_type = PhaseType.BUILD
    has_build_cost = True
    has_description = True
    victory_points = 0


class WallMerchantTest(CastleCardTestBase):
    card_class = WallMerchant
    card_type = CastleCardType.WALL_MERCHANT
    playable_phase_type = PhaseType.BUILD
    has_build_cost = True
    has_description = True
    victory_points = 0


class WallWorkerTest(CastleCardTestBase):
    card_class = WallWorker
    card_type = CastleCardType.WALL_WORKER
    playable_phase_type = PhaseType.BUILD
    has_build_cost = True
    has_description = True
    victory_points = 0


class CastleCardTest(unittest.TestCase):
    def test_lookup(self):
        card = CastleCard(CastleCardType.ADVISOR)

        self.assertEqual(card.card_id, CastleCardType.ADVISOR)

    def test_lookup_error(self):
        with self.assertRaises(InvalidCastleCardTypeError):
            CastleCard('abcdef')

    def test_all_cards_in_map(self):
        self.assertCountEqual(list(CastleCardType.values()),
                              list(CastleCard.card_map.keys()))
