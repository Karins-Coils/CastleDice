import unittest

from .constants import Animals
from .constants import DeckNames
from .constants import DieFaces
from .constants import JoanDieFaces
from .constants import Resources
from .constants import Villagers
from .constants import JOAN
from .constants import JOAN_GATHER_PREFERENCE
from .constants import PHASE


class TestConstants(unittest.TestCase):
    def test_Animals_ordering(self):
        self.assertEqual(
            Animals.values(),
            [Animals.PIG, Animals.HORSE, Animals.CHICKEN, Animals.COW]
        )
        self.assertEqual(
            Animals.keys(),
            ['PIG', 'HORSE', 'CHICKEN', 'COW']
        )

    def test_Resources_ordering(self):
        pass

    def test_Animals_Resources_combined_ordering(self):
        gather_preference = [
                Resources.WOOD,
                Resources.STONE,
                Resources.GOLD,
                Resources.LAND,
                Resources.IRON,
                Animals.PIG,
                Animals.HORSE,
                Animals.CHICKEN,
                Animals.COW,
            ]

        self.assertEqual(
            sorted(Animals.values() + Resources.values()),
            gather_preference
        )
        self.assertEqual(
            JOAN_GATHER_PREFERENCE,
            gather_preference
        )
