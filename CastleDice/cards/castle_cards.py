from CastleDice.cards.exceptions import InvalidCastleCardTypeError
from CastleDice.common.constants import CastleCardType
from CastleDice.common.constants import PhaseType
from CastleDice.common.constants import ResourceType
from CastleDice.common.constants import SpecialPhaseType
from .card_bases import BaseCard
from .card_bases import BuildPhaseMixin
from .card_bases import CardLookupBase
from .card_bases import CastleDeckMixin
from .card_bases import ChoosePhaseMixin
from .card_bases import GatherPhaseMixin
from .card_bases import NoBuildMixin
from .card_bases import NoDescriptionMixin
from .card_bases import NoOngoingMixin
from .card_bases import NoScoreMixin
from .card_bases import NormalDiscardMixin
from .card_bases import ResourceCost


class Advisor(
    CastleDeckMixin,
    NoBuildMixin,
    NoOngoingMixin,
    NoScoreMixin,
    NormalDiscardMixin,
    BaseCard,
):
    _constant = CastleCardType.ADVISOR

    playable_phase = SpecialPhaseType.FIRST_GATHER
    description = (
        "Play before your first gather. Gather one extra time for each Wall you have."
    )

    def is_playable(self):
        raise NotImplementedError()

    def play(self):
        raise NotImplementedError()


class Alchemist(
    CastleDeckMixin,
    BuildPhaseMixin,
    NoBuildMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    BaseCard,
):
    _constant = CastleCardType.ALCHEMIST

    description = (
        "Play during the Build phase. Roll one of each die. Lower the cost of any one "
        "card you want to build this turn by the results. (Animals and Barbarians you "
        "roll have not effect"
    )

    def is_playable(self):
        raise NotImplementedError()

    def play(self):
        raise NotImplementedError()


class Daughter(
    CastleDeckMixin,
    GatherPhaseMixin,
    NoBuildMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    BaseCard,
):
    _constant = CastleCardType.DAUGHTER

    description = (
        "Play before you gather.  Choose one: either your gather this round counts as "
        "a PorkChop, or perform the Villager Choice ability."
    )

    def is_playable(self):
        raise NotImplementedError()

    def play(self):
        raise NotImplementedError()


class DeepMoat(CastleDeckMixin, BuildPhaseMixin, NormalDiscardMixin, BaseCard):
    _constant = CastleCardType.DEEP_MOAT

    description = (
        "Once per turn, when you gather an Animal, you may choose to get ONE of that "
        "die's resource instead."
    )
    ongoing_phase = PhaseType.GATHER
    victory_points = 2
    build_cost = (
        ResourceCost(ResourceType.WOOD, 3),
        ResourceCost(ResourceType.STONE, 2),
        ResourceCost(ResourceType.GOLD, 2),
        ResourceCost(ResourceType.IRON, 2),
    )

    def is_playable(self):
        # confirm is build phase
        # confirm the user has all building materials available
        raise NotImplementedError()

    def play(self):
        # confirm the user has all building materials available
        raise NotImplementedError()

    def can_use_ongoing(self):
        # check if user CAN gather an animal
        # can only be used once per turn, so store state if used this turn
        raise NotImplementedError()

    def has_ongoing_choice(self):
        # offer user the ability to use deep moat
        raise NotImplementedError()

    def reset_ongoing(self):
        # clear state after each turn
        raise NotImplementedError()

    def use_ongoing(self):
        # allow user to select die that contain animals to gather that resource
        raise NotImplementedError()

    def score(self):
        raise NotImplementedError()


class GateHouse(
    CastleDeckMixin,
    BuildPhaseMixin,
    NoDescriptionMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    BaseCard,
):
    _constant = CastleCardType.GATE_HOUSE

    victory_points = 2
    build_cost = (
        ResourceCost(ResourceType.STONE, 2),
        ResourceCost(ResourceType.GOLD, 4),
        ResourceCost(ResourceType.LAND, 2),
    )

    def score(self):
        # no extra scoring rules for this card
        return self.victory_points

    def is_playable(self):
        # if build phase, then playable
        raise NotImplementedError()

    def play(self):
        # deduct build materials and place on mat
        raise NotImplementedError()


class GreatHall(
    CastleDeckMixin,
    BuildPhaseMixin,
    NoDescriptionMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    BaseCard,
):
    _constant = CastleCardType.GREAT_HALL

    victory_points = 3
    build_cost = (
        ResourceCost(ResourceType.STONE, 4),
        ResourceCost(ResourceType.GOLD, 4),
        ResourceCost(ResourceType.LAND, 2),
        ResourceCost(ResourceType.IRON, 2),
    )

    def score(self):
        # no extra scoring rules for this card
        return self.victory_points

    def is_playable(self):
        # if build phase, then playable
        raise NotImplementedError()

    def play(self):
        # deduct build materials and place on mat
        raise NotImplementedError()


class LoyalBrother(
    CastleDeckMixin,
    ChoosePhaseMixin,
    NoBuildMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    BaseCard,
):
    _constant = CastleCardType.LOYAL_BROTHER

    description = (
        "Play before you pick your Choice dice. Add 5 to the number of Choice dice you"
        " get to pick this turn instead of rolling the fixed dice on the Turn Tracker."
    )

    def is_playable(self):
        raise NotImplementedError()

    def play(self):
        raise NotImplementedError()


class RoyalChambers(CastleDeckMixin, BuildPhaseMixin, NormalDiscardMixin, BaseCard):
    _constant = CastleCardType.ROYAL_CHAMBERS

    victory_points = 1
    description = "Pick one extra Choice die to roll each turn"
    ongoing_phase = PhaseType.CHOOSE
    build_cost = (
        ResourceCost(ResourceType.WOOD, 3),
        ResourceCost(ResourceType.STONE, 1),
        ResourceCost(ResourceType.GOLD, 1),
    )

    def is_playable(self):
        # confirm is build phase
        # confirm the user has all building materials available
        raise NotImplementedError()

    def play(self):
        # confirm the user has all building materials available
        raise NotImplementedError()

    def can_use_ongoing(self):
        # check if user CAN gather an animal
        # can only be used once per turn, so store state if used this turn
        raise NotImplementedError()

    def has_ongoing_choice(self):
        # offer user the ability to use deep moat
        raise NotImplementedError()

    def reset_ongoing(self):
        # clear state after each turn
        raise NotImplementedError()

    def use_ongoing(self):
        # allow user to select die that contain animals to gather that resource
        raise NotImplementedError()

    def score(self):
        raise NotImplementedError()


class Squire(
    CastleDeckMixin,
    GatherPhaseMixin,
    NoBuildMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    BaseCard,
):
    _constant = CastleCardType.SQUIRE

    description = (
        "Play instead of gathering. Gain 1 of each resource where you have a guard."
    )

    def is_playable(self):
        # if build phase, then playable
        raise NotImplementedError()

    def play(self):
        # deduct build materials and place on mat
        raise NotImplementedError()


class StrongTower(
    CastleDeckMixin, BuildPhaseMixin, NormalDiscardMixin, NoOngoingMixin, BaseCard
):
    _constant = CastleCardType.STRONG_TOWER

    victory_points = 3
    description = (
        "Strong Tower costs 1 less Wood, Stone and Gold for each wall you have."
    )
    build_cost = (
        ResourceCost(ResourceType.WOOD, 5),
        ResourceCost(ResourceType.STONE, 5),
        ResourceCost(ResourceType.GOLD, 5),
        ResourceCost(ResourceType.IRON, 2),
    )

    def score(self):
        # no extra scoring rules for this card
        return self.victory_points

    def is_playable(self):
        # if build phase, then playable
        raise NotImplementedError()

    def play(self):
        # deduct build materials and place on mat
        raise NotImplementedError()


class TallKeep(
    CastleDeckMixin, BuildPhaseMixin, NoOngoingMixin, NormalDiscardMixin, BaseCard
):
    _constant = CastleCardType.TALL_KEEP

    victory_points = 4
    description = "Tall Keep costs 1 less of each resource for each Wall you have."
    build_cost = (
        ResourceCost(ResourceType.WOOD, 6),
        ResourceCost(ResourceType.STONE, 6),
        ResourceCost(ResourceType.GOLD, 6),
        ResourceCost(ResourceType.LAND, 6),
        ResourceCost(ResourceType.IRON, 6),
    )

    def score(self):
        # no extra scoring rules for this card
        return self.victory_points

    def is_playable(self):
        # if build phase, then playable
        raise NotImplementedError()

    def play(self):
        # deduct build materials and place on mat
        raise NotImplementedError()


class WallAnimal(
    CastleDeckMixin, BuildPhaseMixin, NormalDiscardMixin, NoOngoingMixin, BaseCard
):
    _constant = CastleCardType.WALL_ANIMAL

    victory_points = 0
    description = (
        "When you build this card, choose an animal type. This card gives you +1 when "
        "deciding who has the most of that animal type."
    )
    build_cost = (
        ResourceCost(ResourceType.WOOD, 1),
        ResourceCost(ResourceType.STONE, 3),
    )

    # TODO: how can i hook into the final game scoring with this card?
    # Track the animal type on this card... and then add it to the totals at the end...?

    def score(self):
        # no extra scoring rules for this card
        raise NotImplementedError()

    def is_playable(self):
        # if build phase, then playable
        raise NotImplementedError()

    def play(self):
        # deduct build materials and place on mat
        raise NotImplementedError()


class WallFarmer(
    CastleDeckMixin, BuildPhaseMixin, NormalDiscardMixin, NoOngoingMixin, BaseCard
):
    _constant = CastleCardType.WALL_FARMER

    victory_points = 0
    description = "If you have 3 Farmers at the end of the game, gain 1 Victory Point."
    build_cost = (
        ResourceCost(ResourceType.WOOD, 1),
        ResourceCost(ResourceType.STONE, 3),
    )

    def score(self):
        # check player's count of Farmers
        # if 3, then vp = 1, else vp = 0 (default)
        raise NotImplementedError()

    def is_playable(self):
        # if build phase, then playable
        raise NotImplementedError()

    def play(self):
        # deduct build materials and place on mat
        raise NotImplementedError()


class WallGuard(
    CastleDeckMixin, BuildPhaseMixin, NormalDiscardMixin, NoOngoingMixin, BaseCard
):
    _constant = CastleCardType.WALL_GUARD

    victory_points = 0
    description = "If you have 5 Guards at the end of the game, gain 1 Victory Point."
    build_cost = (
        ResourceCost(ResourceType.WOOD, 1),
        ResourceCost(ResourceType.STONE, 3),
    )

    def score(self):
        # check player's count of Guards
        # if 5, then vp = 1, else vp = 0 (default)
        raise NotImplementedError()

    def is_playable(self):
        # if build phase, then playable
        raise NotImplementedError()

    def play(self):
        # deduct build materials and place on mat
        raise NotImplementedError()


class WallMerchant(
    CastleDeckMixin, BuildPhaseMixin, NormalDiscardMixin, NoOngoingMixin, BaseCard
):
    _constant = CastleCardType.WALL_MERCHANT

    victory_points = 0
    description = (
        "If you have 3 Merchants at the end of the game, gain 1 Victory Point."
    )
    build_cost = (
        ResourceCost(ResourceType.WOOD, 1),
        ResourceCost(ResourceType.STONE, 3),
    )

    def score(self):
        # check player's count of Merchants
        # if 3, then vp =1, else vp = 0 (default)
        raise NotImplementedError()

    def is_playable(self):
        # if build phase, then playable
        raise NotImplementedError()

    def play(self):
        # deduct build materials and place on mat
        raise NotImplementedError()


class WallWorker(
    CastleDeckMixin, BuildPhaseMixin, NormalDiscardMixin, NoOngoingMixin, BaseCard
):
    _constant = CastleCardType.WALL_WORKER

    victory_points = 0
    description = "If you have 5 Workers at the end of the game, gain 1 Victory Point."
    build_cost = (
        ResourceCost(ResourceType.WOOD, 1),
        ResourceCost(ResourceType.STONE, 3),
    )

    def score(self):
        # check player's count of Workers
        # if 5, then vp =1, else vp = 0 (default)
        raise NotImplementedError()

    def is_playable(self):
        # if build phase, then playable
        raise NotImplementedError()

    def play(self):
        # deduct build materials and place on mat
        raise NotImplementedError()


class CastleCard(CardLookupBase):
    card_map = {
        CastleCardType.ADVISOR: Advisor,
        CastleCardType.ALCHEMIST: Alchemist,
        CastleCardType.DAUGHTER: Daughter,
        CastleCardType.DEEP_MOAT: DeepMoat,
        CastleCardType.GATE_HOUSE: GateHouse,
        CastleCardType.GREAT_HALL: GreatHall,
        CastleCardType.LOYAL_BROTHER: LoyalBrother,
        CastleCardType.ROYAL_CHAMBERS: RoyalChambers,
        CastleCardType.SQUIRE: Squire,
        CastleCardType.STRONG_TOWER: StrongTower,
        CastleCardType.TALL_KEEP: TallKeep,
        CastleCardType.WALL_ANIMAL: WallAnimal,
        CastleCardType.WALL_FARMER: WallFarmer,
        CastleCardType.WALL_GUARD: WallGuard,
        CastleCardType.WALL_MERCHANT: WallMerchant,
        CastleCardType.WALL_WORKER: WallWorker,
    }
    card_lookup_error = InvalidCastleCardTypeError
