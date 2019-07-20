import unittest

from ..named_types import NamedFloat
from ..named_types import NamedInt
from ..named_types import NamedStr
from ..named_types import NamedType
from ..named_types import _named_types
from ..named_types import create_named_type


class BaseTest(unittest.TestCase):
    def _confirm_assertions(self, assertions):
        """
        :param assertions list(tuple): tuples - (expected, actual)
        """
        for idx, assertion in enumerate(assertions):
            with self.subTest(i=idx):
                expected, actual = assertion
                self.assertEqual(expected, actual)


class TestNamedTypesInstanceOf(BaseTest):
    def test_instance_of_builtin(self):
        assertions = [
            # (expected, actual)
            (True, isinstance(NamedStr('x', 'a'), str)),
            (True, isinstance(NamedFloat('x', 1.3), float)),
            (True, isinstance(NamedInt('x', 5), int)),
        ]

        self._confirm_assertions(assertions)

    def test_instance_of_NamedType(self):
        assertions = [
            # (actual, expected)
            (isinstance(NamedStr('x', 'a'), NamedType), True),
            (isinstance(NamedFloat('x', 1.3), NamedType), True),
            (isinstance(NamedInt('x', 5), NamedType), True),
        ]

        self._confirm_assertions(assertions)

    def test_instance_of_self(self):
        assertions = [
            # (actual, expected)
            (isinstance(NamedStr('x', 'a'), NamedStr), True),
            (isinstance(NamedFloat('x', 1.3), NamedFloat), True),
            (isinstance(NamedInt('x', 5), NamedInt), True),
        ]

        self._confirm_assertions(assertions)

    def test_not_instances_of_other_types(self):
        assertions = [
            # (actual, expected)
            (isinstance(NamedStr('x', 'a'), int), False),
            (isinstance(NamedFloat('x', 1.3), int), False),
            (isinstance(NamedInt('x', 5), str), False),
        ]

        self._confirm_assertions(assertions)


class TestNamedTypesComparisons(BaseTest):
    def test_compare_equals(self):
        x = 'some_name'
        assertions = [
            # (actual, expected)
            (NamedStr(x, 'a') == NamedStr(x, 'a'), True),
            (NamedStr(x, 'a') == NamedStr(x, 'apple'), False),
            (NamedStr(x, 'a') != NamedStr(x, 'apple'), True),
            (NamedInt(x, 1) == NamedInt(x, 1), True),
            (NamedInt(x, 12) == NamedInt(x, 1), False),
            (NamedInt(x, 12) != NamedInt(x, 1), True),
            (NamedFloat(x, 1.5) == NamedFloat(x, 1.5), True),
            (NamedFloat(x, 12.1) == NamedFloat(x, 1.5), False),
            (NamedFloat(x, 12.1) != NamedFloat(x, 1.5), True),
        ]
        self._confirm_assertions(assertions)

    def test_compare_greater_less_than(self):
        x = 'some_name'
        assertions = [
            # (actual, expected)
            (NamedStr(x, 'a') < NamedStr(x, 'a'), False),
            (NamedStr(x, 'a') < NamedStr(x, 'apple'), True),
            (NamedStr(x, 'a') > NamedStr(x, 'apple'), False),
            (NamedInt(x, 1) < NamedInt(x, 1), False),
            (NamedInt(x, 12) < NamedInt(x, 1), False),
            (NamedInt(x, 12) > NamedInt(x, 1), True),
            (NamedFloat(x, 1.5) < NamedFloat(x, 1.5), False),
            (NamedFloat(x, 12.1) < NamedFloat(x, 1.5), False),
            (NamedFloat(x, 12.1) > NamedFloat(x, 1.5), True),
        ]
        self._confirm_assertions(assertions)

    def test_compare_greater_less_than_or_equal(self):
        x = 'some_name'
        assertions = [
            # (actual, expected)
            (NamedStr(x, 'a') <= NamedStr(x, 'a'), True),
            (NamedStr(x, 'a') <= NamedStr(x, 'apple'), True),
            (NamedStr(x, 'a') >= NamedStr(x, 'apple'), False),
            (NamedInt(x, 1) <= NamedInt(x, 1), True),
            (NamedInt(x, 12) <= NamedInt(x, 1), False),
            (NamedInt(x, 12) >= NamedInt(x, 1), True),
            (NamedFloat(x, 1.5) <= NamedFloat(x, 1.5), True),
            (NamedFloat(x, 12.1) <= NamedFloat(x, 1.5), False),
            (NamedFloat(x, 12.1) >= NamedFloat(x, 1.5), True),
        ]
        self._confirm_assertions(assertions)

    def test_compare_across_types(self):
        # id(float) < (id(int)) < id(str)
        x = 'some_name'
        assertions = [
            # (actual, expected)
            (NamedStr(x, 'a') <= NamedInt(x, 1), False),
            (NamedStr(x, 'a') > NamedInt(x, 1), True),
            (NamedStr(x, 'a') == NamedInt(x, 1), False),
            (NamedStr(x, 'a') <= NamedFloat(x, 1.5), False),
            (NamedStr(x, 'a') >= NamedFloat(x, 1.5), True),
            (NamedStr(x, 'a') != NamedFloat(x, 1.5), True),
            (NamedInt(x, 1) <= NamedFloat(x, 1.5), True),
            (NamedInt(x, 1) > NamedFloat(x, 1.5), False),
            (NamedInt(x, 1) == NamedFloat(x, 1.5), False),
        ]
        self._confirm_assertions(assertions)

    def test_keep_float_int_comparisons(self):
        x = 'some_name'
        assertions = [
            # (actual, expected)
            (NamedFloat(x, 1.0) == NamedInt(x, 1), True),
            (NamedFloat(x, 1.5) > NamedInt(x, 1), True),
            (NamedFloat(x, 1.2) != NamedInt(x, 1), True),
            (NamedInt(x, 1) <= NamedFloat(x, 1.5), True),
            (NamedInt(x, 1) >= NamedFloat(x, 1.5), False),
            (NamedInt(x, 1) < NamedFloat(x, 1.5), True),
        ]
        self._confirm_assertions(assertions)


class TestNamedTypeCreation(BaseTest):
    def test_get_existing_named_types(self):
        assertions = [
            # (actual, expected)
            (create_named_type(float), NamedFloat),
            (create_named_type(int), NamedInt),
            (create_named_type(str), NamedStr),
        ]
        self._confirm_assertions(assertions)

    def test_new_type_added_to_map(self):
        named_complex = create_named_type(complex)

        self.assertEqual(named_complex, create_named_type(complex))
        self.assertIn(complex, _named_types)
