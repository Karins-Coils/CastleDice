import unittest

from castledice.common.constants import ResourceType, VillagerCardType

from ..card_bases import (
    BaseCard,
    BuildPhaseMixin,
    CardLookupBase,
    CastleDeckMixin,
    ChoosePhaseMixin,
    GatherPhaseMixin,
    MarketDeckMixin,
    NoBuildMixin,
    NoDescriptionMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    ResourceCost,
    VillagerDeckMixin,
)


class ResourceCostTest(unittest.TestCase):
    def test_success(self):
        wood_cost = ResourceCost(ResourceType.WOOD, 3)

        self.assertEqual(wood_cost.resource, ResourceType.WOOD)
        self.assertEqual(wood_cost.amount, 3)


class BaseCardTest(unittest.TestCase):
    def test_abstract_requires_all_the_things(self):
        parents_tests = [
            (
                GatherPhaseMixin,
                CastleDeckMixin,
                NoOngoingMixin,
                NoBuildMixin,
                NoScoreMixin,
            ),
            (
                BuildPhaseMixin,
                MarketDeckMixin,
                NoOngoingMixin,
                NoBuildMixin,
                NoScoreMixin,
            ),
            (
                ChoosePhaseMixin,
                VillagerDeckMixin,
                NoOngoingMixin,
                NoBuildMixin,
                NoScoreMixin,
            ),
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
            BaseCard,
        ):
            _constant = VillagerCardType.WISE_GRANDFATHER

            def description(self):
                return "Some description"

            def is_playable(self):
                return True

            def play(self):
                return

        self.assertTrue(ImplementedCard())

        card = ImplementedCard()
        self.assertEqual(card.card_id, VillagerCardType.WISE_GRANDFATHER)
        self.assertEqual(card.name, "Wise Grandfather")


class CardLookupBaseTest(unittest.TestCase):
    def setUp(self):
        class SomeCard(object):
            A = 1

        class SomeError(Exception):
            pass

        class SomeLookup(CardLookupBase):
            card_map = {"SomeCard": SomeCard}
            card_lookup_error = SomeError

        self.SomeCard = SomeCard
        self.SomeLookup = SomeLookup
        self.SomeError = SomeError

    def test_success(self):
        result = self.SomeLookup("SomeCard")
        self.assertIsInstance(result, self.SomeCard)
        self.assertEqual(result.A, self.SomeCard.A)

    def test_failure(self):
        with self.assertRaises(self.SomeError):
            self.SomeLookup("NotReal")

    def test_child_must_implement(self):
        class NoMap(CardLookupBase):
            card_lookup_error = self.SomeError

        class NoError(CardLookupBase):
            card_map = {"SomeCard": self.SomeCard}

        class NothingAdded(CardLookupBase):
            pass

        for cls in [NoMap, NoError, NothingAdded]:
            with self.assertRaises(NotImplementedError):
                cls("SomeCard")
