"""
Borrowed heavily from https://github.com/hmeine/named_constants
Made tweaks for python 3 compatibility
Also expanded and added functions for my own usages
"""

import inspect
from enum import IntEnum
from typing import Iterator, List, Sequence, Tuple, TypeVar, Union

from .named_types import NamedFloat, NamedInt, NamedStr, create_named_type

__all__ = ["Constants", "StrCase"]


NamedTypeTyping = TypeVar("NamedTypeTyping", NamedFloat, NamedInt, NamedStr)


class StrCase(IntEnum):
    UPPER = 1
    LOWER = 2
    FIRST_CAPITALIZED = 3


class _ConstantsMeta(type):
    def __new__(mcs, name, bases, dct):
        constants = {}

        # replace class contents with values wrapped in (typed) const-class:
        for member in dct:
            value = dct[member]
            if (
                member.startswith("_")
                or inspect.isfunction(value)
                or inspect.ismethoddescriptor(value)
            ):
                continue
            const_cls = create_named_type(type(value))
            c = const_cls(member, value)
            constants[member] = c
            dct[member] = c

        dct["__constants__"] = constants
        dct["__values_dict__"] = dict(
            (value.value, value) for value in constants.values()
        )

        result = type.__new__(mcs, name, bases, dct)

        # support namespace prefix in __repr__ by connecting the namespace here:
        for c in constants.values():
            c._namespace = result

        return result

    def __len__(self) -> int:
        return len(self.__constants__)

    def __iter__(self) -> Iterator[NamedTypeTyping]:
        return iter(self.__constants__.values())

    def __setattr__(self, _name, _value):
        raise TypeError("Constants are not supposed to be changed ex post")

    def __contains__(self, x: Union[str, NamedTypeTyping]) -> bool:
        return self.has_k(x) or self.has_v(x)

    def has_k(self, key: str) -> bool:
        """
        Renamed from has_key, to not be confused for python builtin which is being deprecated
        """
        return key in self.__constants__

    def has_v(self, value: NamedTypeTyping) -> bool:
        return value in self.__constants__.values()

    def keys(self) -> List[str]:
        return list(self.__constants__.keys())

    def names(self) -> List[str]:
        """Shortcut function to use self.keys(), since the keys are names, and its a shorthand"""
        return self.keys()

    def values(self) -> List[NamedTypeTyping]:
        return list(self.__constants__.values())

    def bare_values(self) -> List[Union[float, int, str]]:
        """Useful when storing in a db, etc"""
        return [c.value for c in self.__constants__.values()]

    def items(self) -> List[Tuple[str, NamedTypeTyping]]:
        return list(self.__constants__.items())

    def bare_items(self) -> List[Tuple[str, Union[float, int, str]]]:
        return [(name, c.value) for name, c in self.__constants__.items()]

    def django_choices(
        self, case: StrCase = StrCase.FIRST_CAPITALIZED
    ) -> Sequence[Tuple[Union[float, int, str], str]]:
        """Converts a Constants into a django model choices compatible tuple.

        Example:
        class YearInSchool(Constants):
            FRESHMAN = 'FR'
            SOPHOMORE = 'SO'
            JUNIOR = 'JR'
            SENIOR = 'SR'
            OTHER = 1

        YEAR_IN_SCHOOL_CHOICES = [
            # (stored_value, ui_value)
            ('FR', 'Freshman'),
            ('SO', 'Sophomore'),
            ('JR', 'Junior'),
            ('SR', 'Senior'),
            (1, 'Other'),
        ]

        YearInSchool.django_choices() == YEAR_IN_SCHOOL_CHOICES

        See test cases for more in-depth examples

        :return: List of tuples to be used in a model choices
        :rtype: Sequence[Tuple[Union[float, int, str], str]]
        """
        choices = []
        for name, value in self.bare_items():
            # first replace any underscores with spaces
            word_name = name.replace("_", " ")

            if case == StrCase.FIRST_CAPITALIZED:
                case_name = word_name.capitalize()
            elif case == StrCase.LOWER:
                case_name = word_name.lower()
            elif case == StrCase.UPPER:
                case_name = word_name.upper()
            else:
                raise ValueError("Unrecognized case %s passed into function" % case)

            choices.append((value, case_name))

        return choices


class Constants(metaclass=_ConstantsMeta):
    """Base class for constant namespaces."""

    # __slots__ = ()

    def __new__(cls, x, case_sensitive=True):
        values_to_check = (x,)
        if not case_sensitive and isinstance(x, str):
            # will check for 3 other cases in values: lower, UPPER, Title
            # this allows for variations in casing ONLY
            values_to_check = (x, x.lower(), x.upper(), x.title())

        for v in values_to_check:
            if cls.has_v(v):
                return cls.__values_dict__[v]
            if cls.has_k(v):
                return cls.__constants__[v]
        raise ValueError("%s has no key or value %r" % (cls.__name__, x))
