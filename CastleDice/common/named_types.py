

__all__ = [
    'named_type',
    'NamedFloat',
    'NamedInt',
    'NamedStr',
]

# TODO: build in comparison dunders to handle classes with values that are str + int mixed?


def _named_value_initial(typ):
    """Returns a 'NamedTyp' class derived from the given 'typ'."""

    def __new__(mcs, name, val):
        res = typ.__new__(mcs, val)
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

    return const


NamedInt = _named_value_initial(int)
NamedStr = _named_value_initial(str)
NamedFloat = _named_value_initial(float)

_named_types = {
    int: NamedInt,
    str: NamedStr,
    float: NamedFloat,
}


def named_type(typ):
    """
    Returns a 'NamedTyp' class derived from the given 'typ'.
    The results are cached, i.e. given the same type, the same
    class will be returned in subsequent calls.
    """
    const = _named_types.get(typ, None)

    if const is None:
        const = _named_value_initial(typ)
        _named_types[typ] = const

    return const
