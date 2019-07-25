import unittest

from django.contrib.auth.models import User

from CastleDice.common.dice import DICE_COUNT
from CastleDice.common.globals import BARN
from CastleDice.common.globals import CHICKEN
from CastleDice.common.globals import COW
from CastleDice.common.globals import GOLD
from CastleDice.common.globals import HORSE
from CastleDice.common.globals import IRON
from CastleDice.common.globals import LAND
from CastleDice.common.globals import PIG
from CastleDice.common.globals import STONE
from CastleDice.common.globals import TURN
from CastleDice.common.globals import WOOD
from CastleDice.game.solo_ai import JoanAI


# Create your tests here.


class TestJoanAI(unittest.TestCase):
    def setUp(self):
        # have at least one user in the database to use against tests below
        u = User.objects.get_or_create(username="test", email="test@test.com")

        self.pool1 = {
            # no Gold
            WOOD: [
                (WOOD, 3),
                (WOOD, 1),
                (COW, 1),
                (WOOD, 2),
                (WOOD, 2),
                (WOOD, 1),
                (WOOD, 1),
            ],
            STONE: [(STONE, 1), (CHICKEN, 1), (STONE, 2)],
            GOLD: [(HORSE, 1)],
            LAND: [(PIG, 1), (LAND, 2), (LAND, 1), (LAND, 1), (PIG, 1)],
            IRON: [(CHICKEN, 1), (IRON, 1), (PIG, 1), (HORSE, 1), (IRON, 2)],
        }
        self.pool2 = {
            # no Iron
            WOOD: [
                (WOOD, 3),
                (WOOD, 1),
                (COW, 1),
                (WOOD, 2),
                (WOOD, 2),
                (WOOD, 1),
                (WOOD, 1),
            ],
            STONE: [(STONE, 1), (CHICKEN, 1), (STONE, 2)],
            GOLD: [(GOLD, 2), (HORSE, 1), (GOLD, 2), (GOLD, 1)],
            LAND: [(PIG, 1), (LAND, 2), (LAND, 1), (LAND, 1), (PIG, 1)],
            IRON: [(CHICKEN, 1)],
        }
        self.pool3 = {
            # no Pig
            WOOD: [
                (WOOD, 3),
                (WOOD, 1),
                (COW, 1),
                (WOOD, 2),
                (WOOD, 2),
                (WOOD, 1),
                (WOOD, 1),
            ],
            STONE: [(STONE, 1), (CHICKEN, 1), (STONE, 2)],
            GOLD: [(GOLD, 2), (HORSE, 1), (GOLD, 2), (GOLD, 1)],
            LAND: [(LAND, 1)],
            IRON: [(CHICKEN, 1), (IRON, 1), (HORSE, 1), (IRON, 2)],
        }

    def test_determine_primary_resource(self):
        test_dict = {WOOD: 2, IRON: 1, LAND: 2, STONE: 3}
        self.assertEqual(JoanAI.determine_primary_resource(test_dict), STONE)

        test_dict = {WOOD: 2, IRON: 1, LAND: 1, STONE: 2}
        self.assertEqual(JoanAI.determine_primary_resource(test_dict), STONE)

        test_dict = {WOOD: 2, IRON: 1, LAND: 2, STONE: 2}
        self.assertEqual(JoanAI.determine_primary_resource(test_dict), LAND)

    def test_gather_dice(self):
        self.assertEqual(JoanAI.gather_die(WOOD, self.pool1), (WOOD, 3))
        self.assertEqual(JoanAI.gather_die(WOOD, self.pool3, BARN), (HORSE, 1))
        self.assertEqual(JoanAI.gather_die(WOOD, self.pool2, IRON), (LAND, 2))
        self.assertNotEqual(JoanAI.gather_die(WOOD, self.pool1, GOLD)[0], GOLD)

    def test_choose_dice(self):
        self.assertEqual(len(JoanAI.choose_dice(1, DICE_COUNT)), TURN[1]["no_choices"])

    def test_get_user_joan(self):
        # Creates new user named Joan
        u = User.objects.order_by("-id")[0]
        joan_created = JoanAI.get_user_joan()
        self.assertEqual(User.objects.get(id=joan_created.id), joan_created)
        self.assertEqual(u.id + 1, joan_created.id)

        # Retrieves existing user Joan
        joan_retrieved = JoanAI.get_user_joan()
        self.assertEqual(joan_created, joan_retrieved)

        last_user = User.objects.order_by("-id")[0]
        self.assertEqual(joan_created.id, last_user.id)
