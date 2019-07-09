from .base_classes import BaseCard
from .base_classes import BuildPhaseMixin
from .base_classes import GatherPhaseMixin
from .base_classes import NoBuildMixin
from .base_classes import NoDescriptionMixin
from .base_classes import NoOngoingMixin
from .base_classes import NoScoreMixin
from .base_classes import NormalDiscardMixin
from .base_classes import ResourceCost
from .base_classes import VillagerDeckMixin
from ..common import Resources
from ..common import VillagerCards


class Farmer(
    BuildPhaseMixin,
    NoDescriptionMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    VillagerDeckMixin,
    BaseCard
):
    _constant = VillagerCards.FARMER

    @property
    def build_cost(self):
        return (
            ResourceCost(Resources.WOOD, 2),
            ResourceCost(Resources.LAND, 1),
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
    BaseCard
):
    _constant = VillagerCards.GUARD

    @property
    def build_cost(self):
        return (
            ResourceCost(Resources.WOOD, 2),
        )

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
    BaseCard
):
    _constant = VillagerCards.KINGS_MESSENGER

    @property
    def description(self):
        return "Play instead of gathering. The next player chooses a Villager type that you " \
               "have room for.  You get that one for free!"

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
    BaseCard
):
    _constant = VillagerCards.MERCHANT

    @property
    def build_cost(self):
        return (
            ResourceCost(Resources.GOLD, 2),
        )

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
    BaseCard
):
    _constant = VillagerCards.SOLDIER

    @property
    def description(self):
        return "Play before you gather.  Reroll all your Barbarians into the world, keeping any " \
               "that come up as Barbarians again."

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
    BaseCard
):
    _constant = VillagerCards.WISE_GRANDFATHER

    @property
    def description(self):
        return "Play before you gather.  Gather one extra time this round. After you've " \
               "collected resources from both of your gatherings, roll those two dice back " \
               "into the world pool."

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
    BaseCard
):
    _constant = VillagerCards.WORKER

    @property
    def build_cost(self):
        return (
            ResourceCost(Resources.WOOD, 1),
            ResourceCost(Resources.STONE, 2),
        )

    def is_playable(self):
        # if current phase is playable phase return True
        raise NotImplementedError()

    def play(self):
        # confirm is_playable
        # subtract build materials
        # add worker to player's set of villagers
        raise NotImplementedError()
