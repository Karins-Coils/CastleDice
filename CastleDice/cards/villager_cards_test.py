import unittest

from .villager_cards import Farmer
from .villager_cards import Soldier
from .villager_cards import Worker


class CardTestBase(unittest.TestCase):
    _card = None

    def setUp(self):
        self.card = self._card()

    def has_description(self):
        self.assertTrue(self.card.description)

    def has_no_description(self):
        self.assertFalse(self.card.description)

    def has_build_cost(self):
        self.assertTrue(self.card.build_cost)

    def has_no_build_cost(self):
        self.assertFalse(self.card.build_cost)
        self.assertEqual(len(self.card.build_cost), 0)

    def _test_base_properties(self):
        self.assertTrue(self.card)
        self.assertTrue(self.card.card_id)
        self.assertTrue(self.card.name)


class SoldierTest(CardTestBase):
    _card = Soldier

    def test_properties(self):
        self._test_base_properties()
        self.has_description()
        self.has_no_build_cost()

    @unittest.skip
    def test_play(self):
        raise NotImplementedError()

    @unittest.skip
    def test_is_playable_true(self):
        raise NotImplementedError()

    @unittest.skip
    def test_is_playable_false(self):
        raise NotImplementedError()


class WorkerTest(CardTestBase):
    _card = Worker

    def test_properties(self):
        self._test_base_properties()
        self.has_no_description()
        self.has_build_cost()

    @unittest.skip
    def test_play(self):
        raise NotImplementedError()

    @unittest.skip
    def test_is_playable_true(self):
        raise NotImplementedError()

    @unittest.skip
    def test_is_playable_false(self):
        raise NotImplementedError()


class FarmerTest(CardTestBase):
    _card = Farmer

    def test_properties(self):
        self._test_base_properties()
        self.has_no_description()
        self.has_build_cost()

    @unittest.skip
    def test_play(self):
        raise NotImplementedError()

    @unittest.skip
    def test_is_playable_true(self):
        raise NotImplementedError()

    @unittest.skip
    def test_is_playable_false(self):
        raise NotImplementedError()
