import unittest

from ..common import DieFaces
from .die import _Die
from .die import _DieSide
from .die import Die
from .die import GoldDie
from .die import IronDie
from .die import JoanDie
from .die import LandDie
from .die import StoneDie
from .die import WoodDie


class DieTest(unittest.TestCase):
    def test_die_lookup(self):
        die_types = [
            # (resource, die)
            (DieFaces.WOOD, WoodDie),
            (DieFaces.STONE, StoneDie),
            (DieFaces.GOLD, GoldDie),
            (DieFaces.LAND, LandDie),
            (DieFaces.IRON, IronDie),
        ]

        for resource, die_type in die_types:
            self.assertTrue(
                isinstance(Die(resource), die_type)
            )

    def test_die_lookup_has_die_functions(self):
        wood_die = Die(DieFaces.WOOD)

        roll = wood_die.roll()
        self.assertIn(roll, wood_die.sides())


class _DieTest(unittest.TestCase):
    def test_sides_required(self):
        with self.assertRaises(NotImplementedError):
            _Die.sides()

    def test_class_method(self):
        self.assertEqual(len(LandDie.sides()), 6)

    def test_sides_are_constant(self):
        wood_die = WoodDie()

        # should create a copy
        sides = wood_die.sides()

        # modifying the copy should NOT touch the underlying on the class
        sides += (None, None)
        self.assertNotEqual(wood_die.sides(), sides)

    def test_roll(self):
        result = JoanDie.roll()

        self.assertIn(result, JoanDie.sides())

        # confirm the resource is a DieFace, and knows its name
        self.assertTrue(isinstance(result, _DieSide))
        self.assertTrue(isinstance(result.resource.name, str))
        self.assertTrue(isinstance(result.amount, int))


class _DieSideTest(unittest.TestCase):
    def test_basics(self):
        side = _DieSide(DieFaces.WOOD, 3)

        self.assertEqual(side.resource, DieFaces.WOOD)
        self.assertEqual(side.amount, 3)
        self.assertEqual(side.value, (DieFaces.WOOD, 3))

    def test_is_barbarian_true(self):
        side = _DieSide(DieFaces.BARBARIAN, 1)

        self.assertTrue(side.is_barbarian())

    def test_is_barbarian_false(self):
        side = _DieSide(DieFaces.HORSE, 1)

        self.assertFalse(side.is_barbarian())
