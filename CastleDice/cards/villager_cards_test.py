import unittest

from .villager_cards import Farmer
from .villager_cards import Guard
from .villager_cards import KingsMessenger
from .villager_cards import Merchant
from .villager_cards import Soldier
from .villager_cards import WiseGrandfather
from .villager_cards import Worker

from ..common import Phases


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
        self.has_playable_phase(Phases.BUILD)

    def has_no_build_cost(self):
        self.assertFalse(self.card.build_cost)
        self.assertEqual(len(self.card.build_cost), 0)

    def has_playable_phase(self, phase):
        self.assertEqual(self.card.playable_phase, phase)

    def _test_base_properties(self):
        self.assertTrue(self.card)
        self.assertTrue(self.card.card_id)
        self.assertTrue(self.card.name)


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


class GuardTest(CardTestBase):
    _card = Guard

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


class KingsMessengerTest(CardTestBase):
    _card = KingsMessenger

    def test_properties(self):
        self._test_base_properties()
        self.has_description()
        self.has_no_build_cost()
        self.has_playable_phase(Phases.GATHER)

    @unittest.skip
    def test_play(self):
        raise NotImplementedError()

    @unittest.skip
    def test_is_playable_true(self):
        raise NotImplementedError()

    @unittest.skip
    def test_is_playable_false(self):
        raise NotImplementedError()


class MerchantTest(CardTestBase):
    _card = Merchant

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


class SoldierTest(CardTestBase):
    _card = Soldier

    def test_properties(self):
        self._test_base_properties()
        self.has_description()
        self.has_no_build_cost()
        self.has_playable_phase(Phases.GATHER)

    @unittest.skip
    def test_play(self):
        raise NotImplementedError()

    @unittest.skip
    def test_is_playable_true(self):
        raise NotImplementedError()

    @unittest.skip
    def test_is_playable_false(self):
        raise NotImplementedError()


class WiseGrandfatherTest(CardTestBase):
    _card = WiseGrandfather

    def test_properties(self):
        self._test_base_properties()
        self.has_description()
        self.has_no_build_cost()
        self.has_playable_phase(Phases.GATHER)

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
