import random

from ..common import DieFace
from ..common import JOAN
from ..common import JoanDieFace
from ..common import ResourceType

__all__ = [
    'Die',
    'DieAlreadyRolledError',
    'JoanDie',
    'GoldDie',
    'InvalidDieSideError',
    'IronDie',
    'LandDie',
    'StoneDie',
    'WoodDie',
]


class DieAlreadyRolledError(Exception):
    """Raised when a die already has a set rolled value"""


class InvalidDieSideError(Exception):
    """When attempting to use a bad _DieSide and Die combination"""


class _DieSide(object):
    _resource = None
    _amount = None

    def __init__(self, resource, amount):
        """
        :param resource (DieFaces):
        :param amount (int):
        """
        self._resource = resource
        self._amount = amount

    @property
    def resource(self):
        """
        :return DieFaces:
        """
        return self._resource

    @property
    def amount(self):
        """
        :return int:
        """
        return self._amount

    @property
    def value(self):
        """
        :return (DieFaces, int):
        """
        return self._resource, self._amount

    def is_barbarian(self):
        return self._resource == DieFace.BARBARIAN


class _Die(object):
    """Non-importable base class.  Should NEVER be used without inheriting and setting _sides"""
    _type = None
    _sides = ()
    _rolled_side = None

    def __init__(self, resource=None, amount=None):
        """
        :param value (_DieSide):
        """
        value = None
        if resource and amount:
            value = self._find_side(resource, amount)

            if not value:
                raise InvalidDieSideError()

        self._rolled_side = value

    @classmethod
    def type(cls):
        """
        :return (common.Resources):
        """
        return cls._type

    def _find_side(self, resource, amount):
        """Locates the first side in Die's _sides that matches parameters

        :param resource (DieFaces):
        :param amount (int):
        :return Optional[_DieSide]:
        """
        for side in self._sides:
            if side.resource == resource and side.amount == amount:
                return side

        return None

    @classmethod
    def sides(cls):
        """
        :return tuple:
        """
        if not len(cls._sides):
            raise NotImplementedError()

        # return copy of sides, just in case.  prevents editing
        return cls._sides[:]

    def _select_random_side(self):
        roll = random.randint(0, len(self._sides) - 1)
        return self._sides[roll]

    def roll(self):
        """Randomly chooses one of the sides.  Sets that value on this die.
        Will raise an error if this die has already been rolled

        :return _DieSide:
        :raises DieAlreadyRolledError: if die has already been rolled
        """
        if self._rolled_side:
            raise DieAlreadyRolledError()

        return self.reroll()

    def reroll(self):
        """Randomly chooses one of the sides.  Sets that value on this die.
        Will overwrite existing rolled value.

        :return:
        """
        self._rolled_side = self._select_random_side()
        return self.value

    @property
    def value(self):
        """
        If, rolled, returns rolled value

        :return _DieSide:
        """
        return self._rolled_side


class WoodDie(_Die):
    _type = ResourceType.WOOD
    _sides = (
        _DieSide(DieFace.WOOD, 1),
        _DieSide(DieFace.WOOD, 1),
        _DieSide(DieFace.WOOD, 2),
        _DieSide(DieFace.WOOD, 3),
        _DieSide(DieFace.COW, 1),
        _DieSide(DieFace.BARBARIAN, 1),
    )


class StoneDie(_Die):
    _type = ResourceType.STONE
    _sides = (
        _DieSide(DieFace.STONE, 1),
        _DieSide(DieFace.STONE, 1),
        _DieSide(DieFace.STONE, 2),
        _DieSide(DieFace.STONE, 2),
        _DieSide(DieFace.CHICKEN, 1),
        _DieSide(DieFace.BARBARIAN, 1),
    )


class GoldDie(_Die):
    _type = ResourceType.GOLD
    _sides = (
        _DieSide(DieFace.GOLD, 1),
        _DieSide(DieFace.GOLD, 1),
        _DieSide(DieFace.GOLD, 1),
        _DieSide(DieFace.GOLD, 2),
        _DieSide(DieFace.HORSE, 1),
        _DieSide(DieFace.BARBARIAN, 1),
    )


class LandDie(_Die):
    _type = ResourceType.LAND
    _sides = (
        _DieSide(DieFace.LAND, 1),
        _DieSide(DieFace.LAND, 1),
        _DieSide(DieFace.LAND, 2),
        _DieSide(DieFace.PIG, 1),
        _DieSide(DieFace.PIG, 1),
        _DieSide(DieFace.BARBARIAN, 1),
    )


class IronDie(_Die):
    _type = ResourceType.IRON
    _sides = (
        _DieSide(DieFace.IRON, 1),
        _DieSide(DieFace.IRON, 2),
        _DieSide(DieFace.CHICKEN, 1),
        _DieSide(DieFace.HORSE, 1),
        _DieSide(DieFace.PIG, 1),
        _DieSide(DieFace.BARBARIAN, 1),
    )


class JoanDie(_Die):
    _type = JOAN
    _sides = (
        _DieSide(JoanDieFace.WOOD, 1),
        _DieSide(JoanDieFace.STONE, 1),
        _DieSide(JoanDieFace.GOLD, 1),
        _DieSide(JoanDieFace.LAND, 1),
        _DieSide(JoanDieFace.IRON, 1),
        _DieSide(JoanDieFace.BARN, 1),
    )


class Die(object):
    """Convenience class for getting a Die by type, if type unknown at lookup"""

    die_map = {
        DieFace.WOOD: WoodDie,
        DieFace.STONE: StoneDie,
        DieFace.GOLD: GoldDie,
        DieFace.LAND: LandDie,
        DieFace.IRON: IronDie,
    }

    def __new__(self, die_type, resource=None, amount=None):
        if die_type in self.die_map:
            return self.die_map[die_type](resource, amount)

        raise TypeError("Unknown resource type, could not find die")
