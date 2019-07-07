from .base_classes import BaseCard
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


class Worker(
    GatherPhaseMixin,
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
        # reroll player's barbarians
        # keep any that were barbarians again
        raise NotImplementedError()


class Farmer(
    GatherPhaseMixin,
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
        # reroll player's barbarians
        # keep any that were barbarians again
        raise NotImplementedError()
