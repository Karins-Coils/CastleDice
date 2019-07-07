import unittest

from .base_classes import BaseCard
from .base_classes import CastleDeckMixin
from .base_classes import MarketDeckMixin
from .base_classes import VillagerDeckMixin
from .base_classes import NormalDiscard
from .base_classes import NoBuildMixin
from .base_classes import NoScoreMixin
from .base_classes import NoOngoingMixin
from .base_classes import GatherPhaseMixin
from .base_classes import BuildPhaseMixin
from .base_classes import ChoosePhaseMixin


class BaseCardTest(unittest.TestCase):
    def test_abstract_requires_all_the_things(self):
        parents_tests = [
            (GatherPhaseMixin, CastleDeckMixin, NoOngoingMixin, NoBuildMixin, NoScoreMixin),
            (BuildPhaseMixin, MarketDeckMixin, NoOngoingMixin, NoBuildMixin, NoScoreMixin),
            (ChoosePhaseMixin, VillagerDeckMixin, NoOngoingMixin, NoBuildMixin, NoScoreMixin),
            (NoScoreMixin, NormalDiscard),
        ]

        for parents in parents_tests:
            class ImplementedCard(*parents, BaseCard):
                pass

            with self.assertRaises(TypeError):
                ImplementedCard()

    def test_implemented_all_the_things(self):
        class ImplementedCard(
            GatherPhaseMixin,
            MarketDeckMixin,
            NoOngoingMixin,
            NormalDiscard,
            NoBuildMixin,
            NoScoreMixin,
            BaseCard
        ):
            def name(self):
                return "This Card"

            def card_id(self):
                return 123

            def description(self):
                return "Some description"

            def is_playable(self):
                return True

            def play(self):
                return

        self.assertTrue(ImplementedCard())
