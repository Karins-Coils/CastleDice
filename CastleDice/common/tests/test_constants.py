import unittest

from .constants import AnimalType
from .constants import DeckName
from .constants import DieFace
from .constants import JoanDieFace
from .constants import ResourceType
from .constants import VillagerType
from .constants import JOAN
from .constants import JOAN_GATHER_PREFERENCE
from .constants import PHASE


class TestConstants(unittest.TestCase):
    def test_Animals_ordering(self):
        self.assertEqual(
            AnimalType.values(),
            [AnimalType.PIG, AnimalType.HORSE, AnimalType.CHICKEN, AnimalType.COW]
        )
        self.assertEqual(
            AnimalType.keys(),
            ['PIG', 'HORSE', 'CHICKEN', 'COW']
        )

    def test_Resources_ordering(self):
        pass

    def test_Animals_Resources_combined_ordering(self):
        gather_preference = [
                ResourceType.WOOD,
                ResourceType.STONE,
                ResourceType.GOLD,
                ResourceType.LAND,
                ResourceType.IRON,
                AnimalType.PIG,
                AnimalType.HORSE,
                AnimalType.CHICKEN,
                AnimalType.COW,
            ]

        self.assertEqual(
            sorted(AnimalType.values() + ResourceType.values()),
            gather_preference
        )
        self.assertEqual(
            JOAN_GATHER_PREFERENCE,
            gather_preference
        )
