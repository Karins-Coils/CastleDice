import random

from ..common import DieFaces
from ..common import JoanDieFaces

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
        return self._resource == DieFaces.BARBARIAN


class _Die(object):
    """Non-importable base class.  Should NEVER be used without inheriting and setting _sides"""
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
    _sides = (
        _DieSide(DieFaces.WOOD, 1),
        _DieSide(DieFaces.WOOD, 1),
        _DieSide(DieFaces.WOOD, 2),
        _DieSide(DieFaces.WOOD, 3),
        _DieSide(DieFaces.COW, 1),
        _DieSide(DieFaces.BARBARIAN, 1),
    )


class StoneDie(_Die):
    _sides = (
        _DieSide(DieFaces.STONE, 1),
        _DieSide(DieFaces.STONE, 1),
        _DieSide(DieFaces.STONE, 2),
        _DieSide(DieFaces.STONE, 2),
        _DieSide(DieFaces.CHICKEN, 1),
        _DieSide(DieFaces.BARBARIAN, 1),
    )


class GoldDie(_Die):
    _sides = (
        _DieSide(DieFaces.GOLD, 1),
        _DieSide(DieFaces.GOLD, 1),
        _DieSide(DieFaces.GOLD, 1),
        _DieSide(DieFaces.GOLD, 2),
        _DieSide(DieFaces.HORSE, 1),
        _DieSide(DieFaces.BARBARIAN, 1),
    )


class LandDie(_Die):
    _sides = (
        _DieSide(DieFaces.LAND, 1),
        _DieSide(DieFaces.LAND, 1),
        _DieSide(DieFaces.LAND, 2),
        _DieSide(DieFaces.PIG, 1),
        _DieSide(DieFaces.PIG, 1),
        _DieSide(DieFaces.BARBARIAN, 1),
    )


class IronDie(_Die):
    _sides = (
        _DieSide(DieFaces.IRON, 1),
        _DieSide(DieFaces.IRON, 2),
        _DieSide(DieFaces.CHICKEN, 1),
        _DieSide(DieFaces.HORSE, 1),
        _DieSide(DieFaces.PIG, 1),
        _DieSide(DieFaces.BARBARIAN, 1),
    )


class JoanDie(_Die):
    _sides = (
        _DieSide(JoanDieFaces.WOOD, 1),
        _DieSide(JoanDieFaces.STONE, 1),
        _DieSide(JoanDieFaces.GOLD, 1),
        _DieSide(JoanDieFaces.LAND, 1),
        _DieSide(JoanDieFaces.IRON, 1),
        _DieSide(JoanDieFaces.BARN, 1),
    )


class Die(object):
    """Convenience class for getting a Die by type, if type unknown at lookup"""

    die_map = {
        DieFaces.WOOD: WoodDie,
        DieFaces.STONE: StoneDie,
        DieFaces.GOLD: GoldDie,
        DieFaces.LAND: LandDie,
        DieFaces.IRON: IronDie,
    }

    def __new__(self, die_type):
        if die_type in self.die_map:
            return self.die_map[die_type]()

        raise TypeError("Unknown resource type, could not find die")
