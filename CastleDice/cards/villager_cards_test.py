import unittest

from .villager_cards import Soldier
from .villager_cards import Worker
from ..common import VillagerCards


class SoldierTest(unittest.TestCase):
    def test_success(self):
        self.assertTrue(Soldier())

    def test_properties(self):
        soldier = Soldier()
        self.assertEqual(soldier.card_id, VillagerCards.SOLDIER)
        self.assertEqual(soldier.name, VillagerCards.SOLDIER.name)
        self.assertTrue(soldier.description)

    @unittest.skip
    def test_play(self):
        raise NotImplementedError()

    @unittest.skip
    def test_is_playable_true(self):
        raise NotImplementedError()

    @unittest.skip
    def test_is_playable_false(self):
        raise NotImplementedError()


class WorkerTest(unittest.TestCase):
    def test_success(self):
        self.assertTrue(Worker())

    def test_properties(self):
        worker = Worker()
        self.assertEqual(worker.card_id, VillagerCards.WORKER)
        self.assertEqual(worker.name, VillagerCards.WORKER.name)
        self.assertTrue(worker.description)

    @unittest.skip
    def test_play(self):
        raise NotImplementedError()

    @unittest.skip
    def test_is_playable_true(self):
        raise NotImplementedError()

    @unittest.skip
    def test_is_playable_false(self):
        raise NotImplementedError()
