from .base_classes import BaseCard
from .base_classes import VillagerDeckMixin
from .base_classes import NormalDiscardMixin
from .base_classes import NoBuildMixin
from .base_classes import NoDescriptionMixin
from .base_classes import NoScoreMixin
from .base_classes import NoOngoingMixin
from .base_classes import GatherPhaseMixin
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
    NoBuildMixin,
    NoDescriptionMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    VillagerDeckMixin,
    BaseCard
):
    _constant = VillagerCards.WORKER

    @property
    def description(self):
        return None

    def is_playable(self):
        # if current phase is playable phase return True
        raise NotImplementedError()

    def play(self):
        # confirm is_playable
        # reroll player's barbarians
        # keep any that were barbarians again
        raise NotImplementedError()
