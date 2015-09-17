import unittest
from django.test import TestCase
from solo_ai import Joan
from CD_globals \
    import Horse, Pig, Cow, Chicken, \
    Barn, Wood, Stone, Gold, Land, Iron

# Create your tests here.


class TestJoan(unittest.TestCase):

    def test_determine_primary_resource(self):
        test_list = [Wood, Wood, Iron, Land, Stone, Stone, Land, Stone]
        self.assertEqual(Joan.determine_primary_resource(test_list), Stone)

        test_list = [Wood, Wood, Iron, Land, Stone, Stone]
        self.assertEqual(Joan.determine_primary_resource(test_list), Stone)

        test_list = [Wood, Wood, Iron, Land, Stone, Stone, Land]
        self.assertEqual(Joan.determine_primary_resource(test_list), Land)
