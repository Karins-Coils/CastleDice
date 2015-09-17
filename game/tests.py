import unittest
from django.test import TestCase
from solo_ai import JoanAI
from CD_globals \
    import HORSE, PIG, COW, CHICKEN, \
    BARN, WOOD, STONE, GOLD, LAND, IRON, DICE_COUNT, TURN

# Create your tests here.


class TestJoanAI(unittest.TestCase):
    def setUp(self):
        self.j_wood = JoanAI(resource=WOOD)
        self.pool1 = {
            # no Gold
            WOOD: [(WOOD, 3), (WOOD, 1), (COW, 1), (WOOD, 2), (WOOD, 2),
                   (WOOD, 1), (WOOD, 1)],
            STONE: [(STONE, 1), (CHICKEN, 1), (STONE, 2)],
            GOLD: [(HORSE, 1)],
            LAND: [(PIG, 1), (LAND, 2), (LAND, 1), (LAND, 1), (PIG, 1)],
            IRON: [(CHICKEN, 1), (IRON, 1), (PIG, 1), (HORSE, 1), (IRON, 2)]
        }
        self.pool2 = {
            # no Iron
            WOOD: [(WOOD, 3), (WOOD, 1), (COW, 1), (WOOD, 2), (WOOD, 2),
                   (WOOD, 1), (WOOD, 1)],
            STONE: [(STONE, 1), (CHICKEN, 1), (STONE, 2)],
            GOLD: [(GOLD, 2), (HORSE, 1), (GOLD, 2), (GOLD, 1)],
            LAND: [(PIG, 1), (LAND, 2), (LAND, 1), (LAND, 1), (PIG, 1)],
            IRON: [(CHICKEN, 1)]
        }
        self.pool3 = {
            # no Pig
            WOOD: [(WOOD, 3), (WOOD, 1), (COW, 1), (WOOD, 2), (WOOD, 2),
                   (WOOD, 1), (WOOD, 1)],
            STONE: [(STONE, 1), (CHICKEN, 1), (STONE, 2)],
            GOLD: [(GOLD, 2), (HORSE, 1), (GOLD, 2), (GOLD, 1)],
            LAND: [(LAND, 1)],
            IRON: [(CHICKEN, 1), (IRON, 1), (HORSE, 1), (IRON, 2)]
        }

    def test_determine_primary_resource(self):
        test_list = [WOOD, WOOD, IRON, LAND, STONE, STONE, LAND, STONE]
        self.assertEqual(JoanAI.determine_primary_resource(test_list), STONE)

        test_list = [WOOD, WOOD, IRON, LAND, STONE, STONE]
        self.assertEqual(JoanAI.determine_primary_resource(test_list), STONE)

        test_list = [WOOD, WOOD, IRON, LAND, STONE, STONE, LAND]
        self.assertEqual(JoanAI.determine_primary_resource(test_list), LAND)

    def test_gather_dice(self):
        self.assertEqual(self.j_wood.gather_die(self.pool1), (WOOD, 3))
        self.assertEqual(self.j_wood.gather_die(self.pool3, BARN), (HORSE, 1))
        self.assertEqual(self.j_wood.gather_die(self.pool2, IRON), (LAND, 2))
        self.assertNotEqual(self.j_wood.gather_die(self.pool1, GOLD)[0], GOLD)

    def test_choose_dice(self):
        self.assertEqual(len(JoanAI.choose_dice(1, DICE_COUNT)),
                         TURN[1]['no_choices'])
