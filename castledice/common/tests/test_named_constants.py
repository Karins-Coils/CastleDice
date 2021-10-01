import unittest

from ..named_constants import Constants
from ..named_constants import StrCase
from ..named_types import NamedFloat
from ..named_types import NamedInt


class MyConstants(Constants):
    pi = 3.141592653589793
    e = 2.718281828459045
    answer = 42
    BOILERPLATE = "This code comes with no warranty."
    EURO_SYMBOL = u"\u20ac"


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


class StringConstant(Constants):
    A = "apple"
    B = "banana"
    C = "carrot"


class BaseTest(unittest.TestCase):
    def _confirm_assertions(self, assertions):
        """
        :param assertions list(tuple): tuples - (actual, expected)
        """
        for idx, assertion in enumerate(assertions):
            with self.subTest(i=idx):
                actual, expected = assertion
                self.assertEqual(expected, actual)


class TestConstants(BaseTest):
    def test_assignment_error(self):
        with self.assertRaises(TypeError):
            Colors.black = None

    def test_ObjectType_has_methods(self):
        assertions = [
            ("read" in ObjectType, False),
            ("other" in ObjectType, False),
            (ObjectType.other(), "test method"),
            (ObjectType.read(1) == ObjectType(1) == ObjectType.Ellipse, True),
        ]

        self._confirm_assertions(assertions)

    def test_Colors(self):
        assertions = [
            # (actual, expected)
            (3 in Colors, True),
            (17 in Colors, False),
            ("blue" in Colors, True),
            ("silver" in Colors, False),
            (Colors.has_v(3), True),
            (Colors.has_v(8), False),
            (Colors.has_v("blue"), False),
            (Colors.has_k("blue"), True),
            (Colors.has_k("purple"), False),
            (Colors.has_k(3), False),
            (Colors.green == 2, True),
            (Colors("white") is Colors.white, True),
            (Colors(3), Colors.blue),
        ]
        self._confirm_assertions(assertions)

    def test_variable_assignment_comparisons(self):
        color1 = 3
        color2 = Colors(color1)
        color3 = Colors("blue")

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
            (type(MyConstants.pi), NamedFloat),
            (type(MyConstants.pi.value), float),
            (MyConstants.pi, 3.141592653589793),
            (MyConstants.pi / 2, 1.5707963267948966),
            (MyConstants.pi.name, "pi"),
        ]
        self._confirm_assertions(assertions)

    def test_dictness(self):
        assertions = [
            # (actual, expected)
            (len(Colors), 5),
            (Colors.values() == list(range(5)) == list(Colors), True),
            (Colors.keys(), ["red", "yellow", "green", "blue", "white"]),
            (
                Colors.items(),
                [("red", 0), ("yellow", 1), ("green", 2), ("blue", 3), ("white", 4)],
            ),
        ]

        self._confirm_assertions(assertions)

    def test_methods(self):
        assertions = [
            # (actual, expected)
            (isinstance(Colors.values()[0], NamedInt), True),
            (isinstance(Colors.values()[0], int), True),  # NamedInt is a subtype of int
            (isinstance(Colors.bare_values()[0], NamedInt), False),
            (isinstance(Colors.bare_values()[0], int), True),
            # key in the tuple - str
            (isinstance(Colors.items()[0][0], str), True),
            (isinstance(Colors.bare_items()[0][0], str), True),
            # value in the tuple - int
            (isinstance(Colors.items()[0][1], NamedInt), True),
            (
                isinstance(Colors.items()[0][1], int),
                True,
            ),  # NamedInt is a subtype of int
            (isinstance(Colors.bare_items()[0][1], NamedInt), False),
            (isinstance(Colors.bare_items()[0][1], int), True),
        ]

        self._confirm_assertions(assertions)

    def test_flexible_key_lookup(self):
        assertions = [
            # (actual, expected)
            (Colors("yellow", case_sensitive=False), Colors.yellow),
            (Colors("Yellow", case_sensitive=False), Colors.yellow),
            (Colors("YELLOW", case_sensitive=False), Colors.yellow),
            (MyConstants("boilerplate", case_sensitive=False), MyConstants.BOILERPLATE),
            (MyConstants("Boilerplate", case_sensitive=False), MyConstants.BOILERPLATE),
            (MyConstants("BOILERPLATE", case_sensitive=False), MyConstants.BOILERPLATE),
        ]
        self._confirm_assertions(assertions)

    def test_non_flexible_key_lookup(self):
        tests = [
            (Colors, "Yellow"),
            (Colors, "YELLOW"),
            (MyConstants, "boilerplate"),
            (MyConstants, "Boilerplate"),
        ]

        for cls, arg in tests:
            with self.assertRaises(ValueError):
                cls(arg)

    def test_flexible_value_lookup(self):
        assertions = [
            (StringConstant("apple"), StringConstant.A),
            (StringConstant("apple", case_sensitive=False), StringConstant.A),
            (StringConstant("Apple", case_sensitive=False), StringConstant.A),
            (StringConstant("APPLE", case_sensitive=False), StringConstant.A),
            # should be a no-op with number values
            (Colors(0), Colors.red),
            (Colors(0, case_sensitive=False), Colors.red),
        ]

        self._confirm_assertions(assertions)

    def test_non_flexible_value_lookup(self):
        tests = [(StringConstant, "APPLE"), (StringConstant, "Apple")]

        for cls, arg in tests:
            with self.assertRaises(ValueError):
                cls(arg)


class TestDjangoChoices(unittest.TestCase):
    def test_default_returns_first_capitalized(self):
        my_constants_choices = [
            (3.141592653589793, "Pi"),
            (2.718281828459045, "E"),
            (42, "Answer"),
            ("This code comes with no warranty.", "Boilerplate"),
            (u"\u20ac", "Euro symbol"),  # this is an odd case we want to test against
        ]

        colors_choices = [
            (0, "Red"),
            (1, "Yellow"),
            (2, "Green"),
            (3, "Blue"),
            (4, "White"),
        ]

        string_constant_choices = [("apple", "A"), ("banana", "B"), ("carrot", "C")]

        self.assertCountEqual(my_constants_choices, MyConstants.django_choices())
        self.assertEqual(colors_choices, Colors.django_choices())
        self.assertEqual(string_constant_choices, StringConstant.django_choices())

        # look at this specific odd case
        self.assertIn((6, "Compoundbegin"), ObjectType.django_choices())

    def test_upper(self):
        my_constants_choices = [
            (3.141592653589793, "PI"),
            (2.718281828459045, "E"),
            (42, "ANSWER"),
            ("This code comes with no warranty.", "BOILERPLATE"),
            (u"\u20ac", "EURO SYMBOL"),  # this is an odd case we want to test against
        ]

        colors_choices = [
            (0, "RED"),
            (1, "YELLOW"),
            (2, "GREEN"),
            (3, "BLUE"),
            (4, "WHITE"),
        ]

        string_constant_choices = [("apple", "A"), ("banana", "B"), ("carrot", "C")]

        self.assertCountEqual(
            my_constants_choices, MyConstants.django_choices(StrCase.UPPER)
        )
        self.assertEqual(colors_choices, Colors.django_choices(StrCase.UPPER))
        self.assertEqual(
            string_constant_choices, StringConstant.django_choices(StrCase.UPPER)
        )

        # look at this specific odd case
        self.assertIn((6, "COMPOUNDBEGIN"), ObjectType.django_choices(StrCase.UPPER))

    def test_lower(self):
        my_constants_choices = [
            (3.141592653589793, "pi"),
            (2.718281828459045, "e"),
            (42, "answer"),
            ("This code comes with no warranty.", "boilerplate"),
            (u"\u20ac", "euro symbol"),  # this is an odd case we want to test against
        ]

        colors_choices = [
            (0, "red"),
            (1, "yellow"),
            (2, "green"),
            (3, "blue"),
            (4, "white"),
        ]

        string_constant_choices = [("apple", "a"), ("banana", "b"), ("carrot", "c")]

        self.assertCountEqual(
            my_constants_choices, MyConstants.django_choices(StrCase.LOWER)
        )
        self.assertEqual(colors_choices, Colors.django_choices(StrCase.LOWER))
        self.assertEqual(
            string_constant_choices, StringConstant.django_choices(StrCase.LOWER)
        )

        # look at this specific odd case
        self.assertIn((6, "compoundbegin"), ObjectType.django_choices(StrCase.LOWER))


class TestOrdering(BaseTest):
    def test_order_of_keys_and_values_respected(self):
        assertions = [
            # (actual, expected)
            (
                MyConstants.keys(),
                [
                    MyConstants.pi.name,
                    MyConstants.e.name,
                    MyConstants.answer.name,
                    MyConstants.BOILERPLATE.name,
                    MyConstants.EURO_SYMBOL.name,
                ],
            ),
            (
                MyConstants.values(),
                [
                    MyConstants.pi.value,
                    MyConstants.e.value,
                    MyConstants.answer.value,
                    MyConstants.BOILERPLATE.value,
                    MyConstants.EURO_SYMBOL.value,
                ],
            ),
            (
                MyConstants.items(),
                [
                    (MyConstants.pi.name, MyConstants.pi.value),
                    (MyConstants.e.name, MyConstants.e.value),
                    (MyConstants.answer.name, MyConstants.answer.value),
                    (MyConstants.BOILERPLATE.name, MyConstants.BOILERPLATE.value),
                    (MyConstants.EURO_SYMBOL.name, MyConstants.EURO_SYMBOL.value),
                ],
            ),
            # the object should NOT have its keys + values sorted by default
            (MyConstants.values() == sorted(MyConstants.values()), False),
            (MyConstants.keys() == sorted(MyConstants.keys()), False),
            (MyConstants.items() == sorted(MyConstants.items()), False),
        ]
        self._confirm_assertions(assertions)

    def test_sorted(self):
        assertions = [
            (
                sorted(MyConstants.keys()),
                [
                    MyConstants.BOILERPLATE.name,
                    MyConstants.EURO_SYMBOL.name,
                    MyConstants.answer.name,
                    MyConstants.e.name,
                    MyConstants.pi.name,
                ],
            ),
            (
                sorted(MyConstants.values()),
                [
                    MyConstants.e.value,
                    MyConstants.pi.value,
                    MyConstants.answer.value,
                    MyConstants.BOILERPLATE.value,
                    MyConstants.EURO_SYMBOL.value,
                ],
            ),
            (
                sorted(Colors.keys()),
                [
                    Colors.blue.name,
                    Colors.green.name,
                    Colors.red.name,
                    Colors.white.name,
                    Colors.yellow.name,
                ],
            ),
            (sorted(Colors.values()), list(range(5))),
        ]

        self._confirm_assertions(assertions)
