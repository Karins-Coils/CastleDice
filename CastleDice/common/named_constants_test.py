import unittest

from .named_constants import Constants
from .named_constants import _named_types


class MyConstants(Constants):
    pi = 3.141592653589793
    e = 2.718281828459045
    answer = 42
    BOILERPLATE = "This code comes with no warranty."
    EURO_SYMBOL = u'\u20ac'


class Colors(Constants):
    red, yellow, green, blue, white = range(5)


class FigConstants(Constants):
    @classmethod
    def read(cls, i):
        return cls(int(i))

    @staticmethod
    def other():
        return "test method"


class ObjectType(FigConstants):
    CustomColor = 0
    Ellipse = 1
    Polygon = 2
    Spline = 3
    Text = 4
    Arc = 5
    CompoundBegin = 6
    CompoundEnd = -6


class Tests(unittest.TestCase):
    def _confirm_assertions(self, assertions):
        """
        :param assertions list(tuple): tuples - (expected, actual)
        """
        for idx, assertion in enumerate(assertions):
            actual, expected = assertion
            self.assertEqual(expected,
                             actual,
                             msg=f"assertion #{idx} failed")

    def test_assignment_error(self):
        with self.assertRaises(TypeError):
            Colors.black = None

    def test_ObjectType_has_methods(self):
        assertions = [
            ('read' in ObjectType, False),
            ('other' in ObjectType, False),
            (ObjectType.other(), 'test method'),
            (ObjectType.read(1) == ObjectType(1) == ObjectType.Ellipse, True)
        ]

        self._confirm_assertions(assertions)

    def test_Colors(self):
        assertions = [
            # (actual, expected)
            (3 in Colors, True),
            (17 in Colors, False),
            ('blue' in Colors, True),
            ('silver' in Colors, False),
            (Colors.has_v(3), True),
            (Colors.has_v(8), False),
            (Colors.has_v('blue'), False),
            (Colors.has_k('blue'), True),
            (Colors.has_k('purple'), False),
            (Colors.has_k(3), False),
            (Colors.green == 2, True),
            (Colors('white') is Colors.white, True),
            (Colors(3), Colors.blue),

        ]
        self._confirm_assertions(assertions)

    def test_variable_assignment_comparisons(self):
        color1 = 3
        color2 = Colors(color1)
        color3 = Colors('blue')

        assertions = [
            # (actual, expected)
            (color1 == color2, True),
            (color1 is color2, False),
            (color2 is Colors.blue, True),
            (color3 is Colors.blue, True),
        ]
        self._confirm_assertions(assertions)

    def test_MyConstants(self):
        assertions = [
            # (actual, expected)
            (str(type(MyConstants.pi)), "<class 'common.named_constants.NamedFloat'>"),
            (type(MyConstants.pi.value), float),
            (MyConstants.pi, 3.141592653589793),
            (MyConstants.pi / 2, 1.5707963267948966),
            (MyConstants.pi.name, 'pi'),
        ]
        self._confirm_assertions(assertions)

    def test_dictness(self):
        assertions = [
            # (actual, expected)
            (len(Colors), 5),
            (Colors.values() == list(range(5)) == list(Colors), True),
            (Colors.keys(), ['red', 'yellow', 'green', 'blue', 'white']),
            (Colors.items(), [('red', 0), ('yellow', 1), ('green', 2), ('blue', 3), ('white', 4)])
        ]

        self._confirm_assertions(assertions)

    def test_methods(self):
        named_int = _named_types.get(int)
        named_str = _named_types.get(str)
        assertions = [
            # (actual, expected)
            (isinstance(Colors.values()[0], named_int), True),
            (isinstance(Colors.values()[0], int), True),  # NamedInt is a subtype of int
            (isinstance(Colors.bare_values()[0], named_int), False),
            (isinstance(Colors.bare_values()[0], int), True),

            # key in the tuple - str
            (isinstance(Colors.items()[0][0], str), True),
            (isinstance(Colors.bare_items()[0][0], str), True),

            # value in the tuple - int
            (isinstance(Colors.items()[0][1], named_int), True),
            (isinstance(Colors.items()[0][1], int), True),  # NamedInt is a subtype of int

            (isinstance(Colors.bare_items()[0][1], named_int), False),
            (isinstance(Colors.bare_items()[0][1], int), True),
        ]

        self._confirm_assertions(assertions)
