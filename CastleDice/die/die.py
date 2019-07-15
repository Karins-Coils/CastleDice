import random
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

from ..common.constants import DieFace
from ..common.constants import JoanDieFace
from ..common.constants import ResourceType
from ..common.setup import JOAN

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
    'roll_dice',
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

    def __init__(self, die_face: Optional[DieFace] = None, amount: Optional[int] = None):
        """
        :param die_face:
        :type: DieFace
        :param amount:
        :type: int
        """
        value = None
        if die_face and amount:
            value = self._find_side(die_face, amount)

            if not value:
                raise InvalidDieSideError()

        self._rolled_side = value

    @classmethod
    def type(cls) -> ResourceType:
        """
        :rtype: ResourceType
        """
        return cls._type

    def _find_side(self, die_face: DieFace, amount: int) -> Optional[_DieSide]:
        """Locates the first side in Die's _sides that matches parameters

        :param die_face:
        :type: DieFaces
        :param amount:
        :type: int
        :rtype: Optional[_DieSide]
        """
        for side in self._sides:
            if side.resource == die_face and side.amount == amount:
                return side

        return None

    @classmethod
    def sides(cls) -> Tuple[_DieSide]:
        """Returns a copy of the tuple of sides.
        :rtype: tuple[_DieSide]
        """
        if not len(cls._sides):
            raise NotImplementedError()

        # return copy of sides, just in case.  prevents editing
        return cls._sides[:]

    def _select_random_side(self) -> _DieSide:
        """Choose a random number based on the total number of sides and
        return the side at that index

        :rtype: _DieSide
        """
        roll = random.randint(0, len(self._sides) - 1)
        return self._sides[roll]

    def roll(self) -> _DieSide:
        """Randomly chooses one of the sides.  Sets that value on this die.
        Will raise an error if this die has already been rolled

        :rtype:_DieSide
        :raises DieAlreadyRolledError: if die has already been rolled
        """
        if self._rolled_side:
            raise DieAlreadyRolledError()

        return self.reroll()

    def reroll(self) -> _DieSide:
        """Randomly chooses one of the sides.  Sets that value on this die.
        Will overwrite existing rolled value.

        :rtype: _DieSide
        """
        self._rolled_side = self._select_random_side()
        return self.value

    @property
    def value(self) -> Optional[_DieSide]:
        """ If, rolled, returns rolled value

        :rtype: Optional[_DieSide]
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

    def __new__(self,
                die_type: ResourceType,
                die_face: Optional[DieFace] = None,
                amount: Optional[int] = None):
        if die_type in self.die_map:
            return self.die_map[die_type](die_face, amount)

        raise TypeError("Unknown resource type, could not find die")


_die_list = Sequence[Union[WoodDie, StoneDie, GoldDie, LandDie, IronDie, JoanDie]]


def roll_dice(dice: _die_list, re_roll: bool = False) -> _die_list:
    """Roll a list of dice.  Only re-rolls a dice if specified.

    :param dice: list of _Die to roll
    :type: Sequence[Union[WoodDie, StoneDie, GoldDie, LandDie, IronDie, JoanDie]]
    :param re_roll: if True, will reroll all die values.
        If False, will raise error if any have previous roll
    :type: bool
    :return: same list of die, with their values rolled
    :rtype: Sequence[Union[WoodDie, StoneDie, GoldDie, LandDie, IronDie, JoanDie]]
    """

    for die in dice:
        if re_roll:
            die.reroll()
        else:
            die.roll()
    return dice
