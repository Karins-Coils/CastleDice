import unittest
from django.test import TestCase
from solo_ai import Joan
from CD_globals \
    import Horse, Pig, Cow, Chicken, \
    Barn, Wood, Stone, Gold, Land, Iron

# Create your tests here.


class TestJoan(unittest.TestCase):
    def setUp(self):
        self.j_wood = Joan(resource=Wood)
        self.pool1 = {
            # no Gold
            Wood: [(Wood, 3), (Wood, 1), (Cow, 1), (Wood, 2), (Wood, 2),
                   (Wood, 1), (Wood, 1)],
            Stone: [(Stone, 1), (Chicken, 1), (Stone, 2)],
            Gold: [(Horse, 1)],
            Land: [(Pig, 1), (Land, 2), (Land, 1), (Land, 1), (Pig, 1)],
            Iron: [(Chicken, 1), (Iron, 1), (Pig, 1), (Horse, 1), (Iron, 2)]
        }
        self.pool2 = {
            # no Iron
            Wood: [(Wood, 3), (Wood, 1), (Cow, 1), (Wood, 2), (Wood, 2),
                   (Wood, 1), (Wood, 1)],
            Stone: [(Stone, 1), (Chicken, 1), (Stone, 2)],
            Gold: [(Gold, 2), (Horse, 1), (Gold, 2), (Gold, 1)],
            Land: [(Pig, 1), (Land, 2), (Land, 1), (Land, 1), (Pig, 1)],
            Iron: [(Chicken, 1)]
        }
        self.pool3 = {
            # no Pig
            Wood: [(Wood, 3), (Wood, 1), (Cow, 1), (Wood, 2), (Wood, 2),
                   (Wood, 1), (Wood, 1)],
            Stone: [(Stone, 1), (Chicken, 1), (Stone, 2)],
            Gold: [(Gold, 2), (Horse, 1), (Gold, 2), (Gold, 1)],
            Land: [(Land, 1)],
            Iron: [(Chicken, 1), (Iron, 1), (Horse, 1), (Iron, 2)]
        }

    def test_determine_primary_resource(self):
        test_list = [Wood, Wood, Iron, Land, Stone, Stone, Land, Stone]
        self.assertEqual(Joan.determine_primary_resource(test_list), Stone)

        test_list = [Wood, Wood, Iron, Land, Stone, Stone]
        self.assertEqual(Joan.determine_primary_resource(test_list), Stone)

        test_list = [Wood, Wood, Iron, Land, Stone, Stone, Land]
        self.assertEqual(Joan.determine_primary_resource(test_list), Land)

    def test_gather_dice(self):
        self.assertEqual(self.j_wood.gather_die(self.pool1), (Wood, 3))
        self.assertEqual(self.j_wood.gather_die(self.pool3, Barn), (Horse, 1))
        self.assertEqual(self.j_wood.gather_die(self.pool2, Iron), (Land, 2))
        self.assertNotEqual(self.j_wood.gather_die(self.pool1, Gold)[0], Gold)