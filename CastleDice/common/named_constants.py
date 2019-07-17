"""
Borrowed heavily from https://github.com/hmeine/named_constants
Made tweaks for python 3 compatibility
Also expanded and added functions for my own usages
"""

import inspect
from enum import IntEnum
from typing import Iterator
from typing import List
from typing import Sequence
from typing import TypeVar
from typing import Tuple
from typing import Union

# TODO: build in comparison dunders to handle classes with values that are str + int mixed?

__all__ = [
    'Constants',
    'StrCase',
]


_named_types = {}
supported_constants_values = Union[str, int, float]
NamedType = TypeVar('NamedType', str, int, float)


class StrCase(IntEnum):
    UPPER = 1
    LOWER = 2
    FIRST_CAPITALIZED = 3


def named_value(typ):
    """Returns a 'NamedTyp' class derived from the given 'typ'.
    The results are cached, i.e. given the same type, the same
    class will be returned in subsequent calls."""
    const = _named_types.get(typ, None)

    if const is None:

        def __new__(inner_mcs, inner_name, val):
            res = typ.__new__(inner_mcs, val)
            res._name = inner_name
            res._value = val
            res._namespace = None
            return res

        @property
        def name(self):
            return self._name

        @property
        def value(self):
            return self._value

        def __repr__(self):
            if self._namespace is None:
                return self._name
            if self._namespace.__module__ in ('__main__', '__builtin__'):
                namespace = self._namespace.__name__
            else:
                namespace = "%s.%s" % (self._namespace.__module__,
                                       self._namespace.__name__)
            return "%s.%s" % (namespace, self._name)

        dct = dict(
            __doc__="""
Named, typed constant (subclassed from original type, cf. `Constants`
class).  Sole purpose is pretty-printing, i.e. __repr__ returns the
constant's name instead of the original string representations.
The name is also available via a `name()` method.""".lstrip(),
            __new__=__new__,
            name=name,
            value=value,
            __repr__=__repr__
        )

        typ_name = typ.__name__
        new_type_name = 'Named' + typ_name[0].upper() + typ_name[1:]
        const = type(new_type_name, (typ, ), dct)

        _named_types[typ] = const

    return const


class _ConstantsMeta(type):
    def __new__(mcs, name, bases, dct):
        constants = {}

        # replace class contents with values wrapped in (typed) const-class:
        for member in dct:
            value = dct[member]
            if (
                member.startswith('_') or
                inspect.isfunction(value) or
                inspect.ismethoddescriptor(value)
            ):
                continue
            const = named_value(type(value))
            c = const(member, value)
            constants[member] = c
            dct[member] = c

        dct['__constants__'] = constants
        dct['__values_dict__'] = dict((value, value) for value in constants.values())
        dct['__sorted__'] = sorted(constants.values(), key=lambda x: (id(type(x)), x))

        result = type.__new__(mcs, name, bases, dct)

        # support namespace prefix in __repr__ by connecting the namespace here:
        for c in constants.values():
            c._namespace = result

        return result

    def __len__(self):
        return len(self.__constants__)

    def __iter__(self):
        return iter(self.__sorted__)

    def __setattr__(self, _name, _value):
        raise TypeError('Constants are not supposed to be changed ex post')

    def __contains__(self, x):
        return self.has_k(x) or self.has_v(x)

    def has_k(self, key):
        """
        Renamed from has_key, to not be confused for python builtin which is being deprecated
        """
        return key in self.__constants__

    def has_v(self, value):
        return value in self.__values_dict__

    def keys(self):
        return [c.name for c in self.__sorted__]

    def values(self):
        return self.__sorted__

    def bare_values(self):
        """Useful when storing in a db, etc"""
        return [c.value for c in self.__sorted__]

    def items(self):
        return [(c.name, c) for c in self.__sorted__]

    def bare_items(self):
        return [(c.name, c.value) for c in self.__sorted__]

    def django_choices(
        self,
        case: StrCase = StrCase.FIRST_CAPITALIZED
    ) -> Sequence[Tuple[supported_constants_values, str]]:
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
        :rtype: Sequence[Tuple[Union[str, int], str]]
        """
        choices = []
        for name, value in self.bare_items():
            # first replace any underscores with spaces
            word_name = name.replace('_', ' ')

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
        values_to_check = (x, )
        if not case_sensitive and isinstance(x, str):
            # will check for 3 other cases in values: lower, UPPER, Title
            # this allows for variations in casing ONLY
            values_to_check = (x, x.lower(), x.upper(), x.title())

        for v in values_to_check:
            if cls.has_v(v):
                return cls.__values_dict__[v]
            if cls.has_k(v):
                return cls.__constants__[v]
        raise ValueError('%s has no key or value %r' % (cls.__name__, x))
