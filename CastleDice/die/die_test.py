import unittest

from .die import Die
from .die import DieAlreadyRolledError
from .die import GoldDie
from .die import InvalidDieSideError
from .die import IronDie
from .die import JoanDie
from .die import LandDie
from .die import StoneDie
from .die import WoodDie
from .die import _Die
from .die import _DieSide
from ..common import DieFace
from ..common import JOAN
from ..common import ResourceType


class DieTest(unittest.TestCase):
    def test_die_lookup(self):
        die_types = [
            # (resource, die)
            (ResourceType.WOOD, WoodDie),
            (ResourceType.STONE, StoneDie),
            (ResourceType.GOLD, GoldDie),
            (ResourceType.LAND, LandDie),
            (ResourceType.IRON, IronDie),
        ]

        for resource, die_type in die_types:
            die = Die(resource)
            self.assertTrue(isinstance(die, die_type))
            self.assertEqual(die.type(), resource)

    def test_die_lookup_with_rolled_value(self):
        die = Die(ResourceType.WOOD, DieFace.BARBARIAN, 1)

        self.assertEqual(die.type(), ResourceType.WOOD)
        self.assertIsNotNone(die.value)
        self.assertEqual(die.value.resource, DieFace.BARBARIAN)
        self.assertEqual(die.value.amount, 1)

    def test_die_lookup_uknown_type(self):
        with self.assertRaises(TypeError):
            Die(JOAN)

    def test_die_lookup_has_die_functions(self):
        wood_die = Die(DieFace.WOOD)

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

    def test_initialized_with_value(self):
        land_die = LandDie(DieFace.LAND, 1)
        self.assertEqual(land_die.value.resource, DieFace.LAND)
        self.assertEqual(land_die.value.amount, 1)

    def test_initialized_with_bad_value(self):
        with self.assertRaises(InvalidDieSideError):
            IronDie(DieFace.STONE, 1)

    def test_roll(self):
        joan_die = JoanDie()
        result = joan_die.roll()

        self.assertIn(result, joan_die.sides())
        self.assertEqual(result, joan_die.value)

        # confirm the resource is a DieFace, and knows its name
        self.assertTrue(isinstance(result, _DieSide))
        self.assertTrue(isinstance(result.resource.name, str))
        self.assertTrue(isinstance(result.amount, int))

    def test_roll_prevents_reroll(self):
        joan_die = JoanDie()
        result = joan_die.roll()

        with self.assertRaises(DieAlreadyRolledError):
            joan_die.roll()

    def test_reroll_resets_value(self):
        stone_die = StoneDie()
        stone_die.roll()

        # second roll should NOT raise an error
        self.assertTrue(stone_die.reroll())

        # cannot compare two rolls are different reliably, as 1 in 6 times they would be equal


class _DieSideTest(unittest.TestCase):
    def test_basics(self):
        side = _DieSide(DieFace.WOOD, 3)

        self.assertEqual(side.resource, DieFace.WOOD)
        self.assertEqual(side.amount, 3)
        self.assertEqual(side.value, (DieFace.WOOD, 3))

    def test_is_barbarian_true(self):
        side = _DieSide(DieFace.BARBARIAN, 1)

        self.assertTrue(side.is_barbarian())

    def test_is_barbarian_false(self):
        side = _DieSide(DieFace.HORSE, 1)

        self.assertFalse(side.is_barbarian())
