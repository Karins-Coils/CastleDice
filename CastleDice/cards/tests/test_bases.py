import unittest

from CastleDice.common import Resources
from CastleDice.common import VillagerCards
from ..bases import BaseCard
from ..bases import BuildPhaseMixin
from ..bases import CardLookupBase
from ..bases import CastleDeckMixin
from ..bases import ChoosePhaseMixin
from ..bases import GatherPhaseMixin
from ..bases import MarketDeckMixin
from ..bases import NoBuildMixin
from ..bases import NoDescriptionMixin
from ..bases import NoOngoingMixin
from ..bases import NoScoreMixin
from ..bases import NormalDiscardMixin
from ..bases import ResourceCost
from ..bases import VillagerDeckMixin


class ResourceCostTest(unittest.TestCase):
    def test_success(self):
        wood_cost = ResourceCost(Resources.WOOD, 3)

        self.assertEqual(wood_cost.resource, Resources.WOOD)
        self.assertEqual(wood_cost.amount, 3)


class BaseCardTest(unittest.TestCase):
    def test_abstract_requires_all_the_things(self):
        parents_tests = [
            (GatherPhaseMixin, CastleDeckMixin, NoOngoingMixin, NoBuildMixin, NoScoreMixin),
            (BuildPhaseMixin, MarketDeckMixin, NoOngoingMixin, NoBuildMixin, NoScoreMixin),
            (ChoosePhaseMixin, VillagerDeckMixin, NoOngoingMixin, NoBuildMixin, NoScoreMixin),
            (NoScoreMixin, NormalDiscardMixin, NoDescriptionMixin),
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
            NormalDiscardMixin,
            NoBuildMixin,
            NoDescriptionMixin,
            NoOngoingMixin,
            NoScoreMixin,
            BaseCard
        ):
            _constant = VillagerCards.WISE_GRANDFATHER

            def description(self):
                return "Some description"

            def is_playable(self):
                return True

            def play(self):
                return

        self.assertTrue(ImplementedCard())

        card = ImplementedCard()
        self.assertEqual(card.card_id, VillagerCards.WISE_GRANDFATHER)
        self.assertEqual(card.name, "Wise Grandfather")


class CardLookupBaseTest(unittest.TestCase):
    def setUp(self):
        class SomeCard(object):
            A = 1

        class SomeError(Exception):
            pass

        class SomeLookup(CardLookupBase):
            card_map = {
                'SomeCard': SomeCard
            }
            card_lookup_error = SomeError

        self.SomeCard = SomeCard
        self.SomeLookup = SomeLookup
        self.SomeError = SomeError

    def test_success(self):
        result = self.SomeLookup('SomeCard')
        self.assertIsInstance(result, self.SomeCard)
        self.assertEqual(result.A, self.SomeCard.A)

    def test_failure(self):
        with self.assertRaises(self.SomeError):
            self.SomeLookup('NotReal')

    def test_child_must_implement(self):
        class NoMap(CardLookupBase):
            card_lookup_error = self.SomeError

        class NoError(CardLookupBase):
            card_map = {'SomeCard': self.SomeCard}

        class NothingAdded(CardLookupBase):
            pass

        for cls in [NoMap, NoError, NothingAdded]:
            with self.assertRaises(NotImplementedError):
                cls('SomeCard')
