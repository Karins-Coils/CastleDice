from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

__all__ = [
    'create_named_type',
    'NamedFloat',
    'NamedInt',
    'NamedStr',
]


class NamedType(object):
    """
    Convenience class that stores the name and value of a previously unnamed type.
    Should ONLY be used imported as type hinting, or created using create_named_type
    """
    __doc__ = "Named type.  Retains most of parent type's properties, with extras for storing a " \
              "name and ability to compare across different NamedType instances."

    def __new__(cls, name, val):
        res = type(val).__new__(cls, val)
        res._type = type(val)
        res._name = name
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

    def __hash__(self) -> int:
        return hash(self.value)

    @staticmethod
    def __named_type_comparator(
            arg: Union['NamedType', float, int, str]
    ) -> Tuple[int, 'NamedType']:
        """In order to better compare two NamedTypes, convert to a tuple of their type id
        and their value
        Example:
            NamedInt(5) --> (13328, 5)  # 13328 might be the id of NamedInt in memory
        """
        return id(type(arg.value)), getattr(arg, 'value', arg)

    def __get_comparators(self, other) -> Tuple:
        """Given an other value (possibly a NamedType, possibly a bare type [str, float, int]),
        returns two values that can be compared"""
        try:
            # we don't check against specific types or instances, in order to preserve
            # builtin cross-type comparisons (like int v float)
            # if the values are not comparable, will trigger TypeError
            self.value <= getattr(other, 'value', other)

            # same base type (int/str/float), but may not both be NamedFloat, etc
            # use other.value if its a NamedType, else use other's value itself
            return self.value, getattr(other, 'value', other)
        except TypeError:
            pass

        # return instead a tuple with (type_id, val) for self + other to allow ordering
        return self.__named_type_comparator(self), self.__named_type_comparator(other)

    def __eq__(self, other) -> bool:
        try:
            return self.value == getattr(other, 'value', other)
        except TypeError:
            self_cmp, other_cmp = self.__get_comparators(other)
            return self_cmp == other_cmp

    def __lt__(self, other) -> bool:
        self_cmp, other_cmp = self.__get_comparators(other)
        return self_cmp < other_cmp

    def __le__(self, other) -> bool:
        self_cmp, other_cmp = self.__get_comparators(other)
        return self_cmp <= other_cmp


def _create_named_type(value_type: Type) -> Union[type, Type[NamedType]]:
    """Given a typed object, convert it to a NamedTyp instance

    Example:
        'a' --> NamedStr('a')
    """

    new_name = 'Named' + value_type.__name__.capitalize()
    # create a new type, using the original type as a base, and adding in the methods of _NamedType
    return type(new_name, (value_type, NamedType), dict(NamedType.__dict__))


# Explicitly create most commonly used named types
NamedInt = _create_named_type(int)
NamedStr = _create_named_type(str)
NamedFloat = _create_named_type(float)

_named_types = {
    int: NamedInt,
    str: NamedStr,
    float: NamedFloat,
}


def create_named_type(typ: Type) -> Type[NamedType]:
    """
    Returns a 'NamedType' class derived from the given 'typ'.
    The results are cached, i.e. given the same type, the same
    class will be returned in subsequent calls.

    Should ALWAYS be used to create a new type from NamedType, rather than creating an
    instance of NamedType itself
    """
    const = _named_types.get(typ, None)

    if const is None:
        const = _create_named_type(typ)
        _named_types[typ] = const

    return const
