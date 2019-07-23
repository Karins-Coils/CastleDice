import unittest
from decimal import Decimal
from typing import Any
from typing import Iterable
from typing import Tuple

from ..named_types import NamedFloat
from ..named_types import NamedInt
from ..named_types import NamedStr
from ..named_types import NamedType
from ..named_types import _named_types
from ..named_types import create_named_type


class BaseTest(unittest.TestCase):
    def _confirm_assertions(self, assertions: Iterable[Tuple[Any, Any]]):
        """
        :param assertions: tuples - (expected, actual)
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
            # (expected, actual)
            (True, isinstance(NamedStr('x', 'a'), NamedType)),
            (True, isinstance(NamedFloat('x', 1.3), NamedType)),
            (True, isinstance(NamedInt('x', 5), NamedType)),
        ]

        self._confirm_assertions(assertions)

    def test_instance_of_self(self):
        assertions = [
            # (expected, actual)
            (True, isinstance(NamedStr('x', 'a'), NamedStr)),
            (True, isinstance(NamedFloat('x', 1.3), NamedFloat)),
            (True, isinstance(NamedInt('x', 5), NamedInt)),
        ]

        self._confirm_assertions(assertions)

    def test_not_instances_of_other_types(self):
        assertions = [
            # (expected, actual)
            (False, isinstance(NamedStr('x', 'a'), int)),
            (False, isinstance(NamedFloat('x', 1.3), int)),
            (False, isinstance(NamedInt('x', 5), str)),
        ]

        self._confirm_assertions(assertions)

    def test_new_named_type(self):
        named_decimal_type = create_named_type(Decimal)
        named_decimal = named_decimal_type('some_name', Decimal(1.0))

        self.assertEqual('NamedDecimal', named_decimal_type.__name__)
        self.assertEqual(named_decimal, 1.0)
        self.assertEqual(named_decimal, NamedFloat('x', 1.0))
        self.assertEqual(named_decimal, Decimal(1.0))


class TestNamedTypesComparisons(BaseTest):
    def test_compare_equals(self):
        x = 'some_name'
        assertions = [
            # (expected, actual)
            (True, NamedStr(x, 'a') == NamedStr(x, 'a')),
            (False, NamedStr(x, 'a') == NamedStr(x, 'apple')),
            (True, NamedStr(x, 'a') != NamedStr(x, 'apple')),
            (True, NamedInt(x, 1) == NamedInt(x, 1)),
            (False, NamedInt(x, 12) == NamedInt(x, 1)),
            (True, NamedInt(x, 12) != NamedInt(x, 1)),
            (True, NamedFloat(x, 1.5) == NamedFloat(x, 1.5)),
            (False, NamedFloat(x, 12.1) == NamedFloat(x, 1.5)),
            (True, NamedFloat(x, 12.1) != NamedFloat(x, 1.5)),
        ]
        self._confirm_assertions(assertions)

    def test_compare_greater_less_than(self):
        x = 'some_name'
        assertions = [
            # (expected, actual)
            (False, NamedStr(x, 'a') < NamedStr(x, 'a')),
            (True, NamedStr(x, 'a') < NamedStr(x, 'apple')),
            (False, NamedStr(x, 'a') > NamedStr(x, 'apple')),
            (False, NamedInt(x, 1) < NamedInt(x, 1)),
            (False, NamedInt(x, 12) < NamedInt(x, 1)),
            (True, NamedInt(x, 12) > NamedInt(x, 1)),
            (False, NamedFloat(x, 1.5) < NamedFloat(x, 1.5)),
            (False, NamedFloat(x, 12.1) < NamedFloat(x, 1.5)),
            (True, NamedFloat(x, 12.1) > NamedFloat(x, 1.5)),
        ]
        self._confirm_assertions(assertions)

    def test_compare_greater_less_than_or_equal(self):
        x = 'some_name'
        assertions = [
            # (expected, actual)
            (True, NamedStr(x, 'a') <= NamedStr(x, 'a')),
            (True, NamedStr(x, 'a') <= NamedStr(x, 'apple')),
            (False, NamedStr(x, 'a') >= NamedStr(x, 'apple')),
            (True, NamedInt(x, 1) <= NamedInt(x, 1)),
            (False, NamedInt(x, 12) <= NamedInt(x, 1)),
            (True, NamedInt(x, 12) >= NamedInt(x, 1)),
            (True, NamedFloat(x, 1.5) <= NamedFloat(x, 1.5)),
            (False, NamedFloat(x, 12.1) <= NamedFloat(x, 1.5)),
            (True, NamedFloat(x, 12.1) >= NamedFloat(x, 1.5)),
        ]
        self._confirm_assertions(assertions)

    def test_compare_across_types(self):
        # id(float) < (id(int)) < id(str)
        x = 'some_name'
        assertions = [
            # (expected, actual)
            (False, NamedStr(x, 'a') <= NamedInt(x, 1)),
            (True, NamedStr(x, 'a') > NamedInt(x, 1)),
            (False, NamedStr(x, 'a') == NamedInt(x, 1)),
            (False, NamedStr(x, 'a') <= NamedFloat(x, 1.5)),
            (True, NamedStr(x, 'a') >= NamedFloat(x, 1.5)),
            (True, NamedStr(x, 'a') != NamedFloat(x, 1.5)),
            (True, NamedInt(x, 1) <= NamedFloat(x, 1.5)),
            (False, NamedInt(x, 1) > NamedFloat(x, 1.5)),
            (False, NamedInt(x, 1) == NamedFloat(x, 1.5)),
        ]
        self._confirm_assertions(assertions)

    def test_keep_float_int_comparisons(self):
        x = 'some_name'
        assertions = [
            # (expected, actual)
            (True, NamedFloat(x, 1.0) == NamedInt(x, 1)),
            (True, NamedFloat(x, 1.5) > NamedInt(x, 1)),
            (True, NamedFloat(x, 1.2) != NamedInt(x, 1)),
            (True, NamedInt(x, 1) <= NamedFloat(x, 1.5)),
            (False, NamedInt(x, 1) >= NamedFloat(x, 1.5)),
            (True, NamedInt(x, 1) < NamedFloat(x, 1.5)),
        ]
        self._confirm_assertions(assertions)


class TestNamedTypeCreation(BaseTest):
    def test_get_existing_named_types(self):
        assertions = [
            # (expected, actual)
            (NamedFloat, create_named_type(float)),
            (NamedInt, create_named_type(int)),
            (NamedStr, create_named_type(str)),
        ]
        self._confirm_assertions(assertions)

    def test_new_type_added_to_map(self):
        named_complex = create_named_type(complex)

        self.assertEqual(named_complex, create_named_type(complex))
        self.assertIn(complex, _named_types)
