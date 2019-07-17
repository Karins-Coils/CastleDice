from typing import Type

__all__ = [
    'named_type',
    'NamedFloat',
    'NamedInt',
    'NamedStr',
]

# TODO: build in comparison dunders to handle classes with values that are str + int mixed?


class _NamedType(type):
    """Convenience class that stores the name and value of a previously unnamed type."""
    __doc__ = "Named type.  Retains most of parent type's properties, with extras for storing a " \
              "name and ability to compare across different NamedType instances. "

    def __new__(mcs, name, val):
        res = type(val).__new__(mcs, val)
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


def _create_named_type(value_type: type):
    """Given a typed object, convert it to a NamedTyp instance

    Example:
        'a' --> NamedStr('a')
    """

    new_name = 'Named' + value_type.__name__.capitalize()
    # create a new type, using the original type as a base, and adding in the methods of _NamedType
    return type(new_name, (value_type, ), dict(_NamedType.__dict__))


# Explicitly create most commonly used named types
NamedInt = _create_named_type(int)
NamedStr = _create_named_type(str)
NamedFloat = _create_named_type(float)

_named_types = {
    int: NamedInt,
    str: NamedStr,
    float: NamedFloat,
}


def named_type(typ: type) -> Type[_NamedType]:
    """
    Returns a 'NamedTyp' class derived from the given 'typ'.
    The results are cached, i.e. given the same type, the same
    class will be returned in subsequent calls.
    """
    const = _named_types.get(typ, None)

    if const is None:
        const = _create_named_type(typ)
        _named_types[typ] = const

    return const
