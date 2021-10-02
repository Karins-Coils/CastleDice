from castledice.common.constants import ResourceType
from castledice.common.constants import VillagerCardType
from .card_bases import BaseCard
from .card_bases import BuildPhaseMixin
from .card_bases import CardLookupBase
from .card_bases import GatherPhaseMixin
from .card_bases import NoBuildMixin
from .card_bases import NoDescriptionMixin
from .card_bases import NoOngoingMixin
from .card_bases import NoScoreMixin
from .card_bases import NormalDiscardMixin
from .card_bases import ResourceCost
from .card_bases import VillagerDeckMixin
from .exceptions import InvalidVillagerCardTypeError


class Farmer(
    BuildPhaseMixin,
    NoDescriptionMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    VillagerDeckMixin,
    BaseCard,
):
    _constant = VillagerCardType.FARMER

    build_cost = (
        ResourceCost(ResourceType.WOOD, 2),
        ResourceCost(ResourceType.LAND, 1),
    )

    def is_playable(self):
        # if current phase is playable phase return True
        raise NotImplementedError()

    def play(self):
        # confirm is_playable
        # subtract build materials
        # add farmer to player's set of villagers
        raise NotImplementedError()


class Guard(
    BuildPhaseMixin,
    NoDescriptionMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    VillagerDeckMixin,
    BaseCard,
):
    _constant = VillagerCardType.GUARD

    build_cost = (ResourceCost(ResourceType.WOOD, 2),)

    def is_playable(self):
        # if current phase is playable phase return True
        raise NotImplementedError()

    def play(self):
        # confirm is_playable
        # subtract build materials
        # add guardian to player's set of villagers
        raise NotImplementedError()


class KingsMessenger(
    GatherPhaseMixin,
    NoBuildMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    VillagerDeckMixin,
    BaseCard,
):
    _constant = VillagerCardType.KINGS_MESSENGER

    description = (
        "Play instead of gathering. The next player chooses a Villager type that you "
        "have room for.  You get that one for free!"
    )

    def is_playable(self):
        # if current phase is playable phase return True
        raise NotImplementedError()

    def play(self):
        # confirm is_playable
        # Skip gather phase this round
        # v1, pick a villager at random and add to player's set of villagers.  (true for solo play)
        # v2, setup player interaction
        raise NotImplementedError()


class Merchant(
    BuildPhaseMixin,
    NoBuildMixin,
    NoDescriptionMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    VillagerDeckMixin,
    BaseCard,
):
    _constant = VillagerCardType.MERCHANT

    build_cost = (ResourceCost(ResourceType.GOLD, 2),)

    def is_playable(self):
        # if current phase is playable phase return True
        raise NotImplementedError()

    def play(self):
        # confirm is_playable
        # subtract build materials
        # add merchant to player's set of villagers
        raise NotImplementedError()


class Soldier(
    GatherPhaseMixin,
    NoBuildMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    VillagerDeckMixin,
    BaseCard,
):
    _constant = VillagerCardType.SOLDIER

    description = (
        "Play before you gather.  Reroll all your Barbarians into the world, keeping "
        "any that come up as Barbarians again."
    )

    def is_playable(self):
        # if current phase is playable phase return True
        raise NotImplementedError()

    def play(self):
        # confirm is_playable
        # reroll player's barbarians
        # keep any that were barbarians again
        raise NotImplementedError()


class WiseGrandfather(
    GatherPhaseMixin,
    NoBuildMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    VillagerDeckMixin,
    BaseCard,
):
    _constant = VillagerCardType.WISE_GRANDFATHER

    description = (
        "Play before you gather.  Gather one extra time this round. After you've "
        "collected resources from both of your gatherings, roll those two dice back "
        "into the world pool."
    )

    def is_playable(self):
        # if current phase is playable phase return True
        raise NotImplementedError()

    def play(self):
        # confirm is_playable
        # allow the player 2 gathers this round
        # collect those resources
        # reroll the dice
        # add those die + resources back to world pool
        raise NotImplementedError()


class Worker(
    BuildPhaseMixin,
    NoDescriptionMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    VillagerDeckMixin,
    BaseCard,
):
    _constant = VillagerCardType.WORKER

    build_cost = (
        ResourceCost(ResourceType.WOOD, 1),
        ResourceCost(ResourceType.STONE, 2),
    )

    def is_playable(self):
        # if current phase is playable phase return True
        raise NotImplementedError()

    def play(self):
        # confirm is_playable
        # subtract build materials
        # add worker to player's set of villagers
        raise NotImplementedError()


class VillagerCard(CardLookupBase):
    card_map = {
        VillagerCardType.SOLDIER: Soldier,
        VillagerCardType.WORKER: Worker,
        VillagerCardType.FARMER: Farmer,
        VillagerCardType.GUARD: Guard,
        VillagerCardType.MERCHANT: Merchant,
        VillagerCardType.KINGS_MESSENGER: KingsMessenger,
        VillagerCardType.WISE_GRANDFATHER: WiseGrandfather,
    }
    card_lookup_error = InvalidVillagerCardTypeError
