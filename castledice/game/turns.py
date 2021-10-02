from dataclasses import dataclass
from typing import Dict, List

from castledice.common.constants import ResourceType
from castledice.common.setup import DICE_COUNT

__all__ = ["InvalidTurnNumberError", "Turn"]


class InvalidTurnNumberError(Exception):
    """Incorrect Turn Number supplied when selecting turn"""


class TurnBase(object):
    turn_number: int
    given_dice: Dict[ResourceType, int]
    number_of_choices: int
    will_go_to_market: bool

    @classmethod
    def create_player_choice_dice_for_turn(cls) -> List[ResourceType]:
        """
        Return list of individual resources that will be the player's default choice die
        """
        resources: List[ResourceType] = []
        for resource_type, count in cls.given_dice.items():
            resources.extend([resource_type] * count)
        return resources

    @classmethod
    def create_dice_bank_for_turn(cls, player_count: int) -> List[ResourceType]:
        """
        Subtract the choice dice from the global dice bank to return list of die players can
        choose from during Choose phase.
        """
        resources: List[ResourceType] = []
        for resource_type, count in DICE_COUNT.items():
            bank_count = count - (cls.given_dice.get(resource_type, 0) * player_count)
            resources.extend([resource_type] * bank_count)

        return resources


class FirstTurn(TurnBase):
    turn_number = 1
    given_dice = {ResourceType.WOOD: 2, ResourceType.STONE: 2, ResourceType.GOLD: 1}
    number_of_choices = 2
    will_go_to_market = False


class SecondTurn(TurnBase):
    turn_number = 2
    given_dice = {ResourceType.WOOD: 1, ResourceType.STONE: 1, ResourceType.GOLD: 2}
    number_of_choices = 3
    will_go_to_market = False


class ThirdTurn(TurnBase):
    turn_number = 3
    given_dice = {ResourceType.WOOD: 3, ResourceType.STONE: 1, ResourceType.GOLD: 1}
    number_of_choices = 3
    will_go_to_market = True


class FourthTurn(TurnBase):
    turn_number = 4
    given_dice = {ResourceType.WOOD: 1, ResourceType.STONE: 2, ResourceType.GOLD: 1}
    number_of_choices = 3
    will_go_to_market = False


class FifthTurn(TurnBase):
    turn_number = 5
    given_dice = {
        ResourceType.WOOD: 1,
        ResourceType.STONE: 1,
        ResourceType.GOLD: 1,
        ResourceType.LAND: 1,
        ResourceType.IRON: 1,
    }
    number_of_choices = 2
    will_go_to_market = True


class SixthTurn(TurnBase):
    turn_number = 6
    given_dice = {ResourceType.WOOD: 2, ResourceType.GOLD: 2, ResourceType.IRON: 2}
    number_of_choices = 3
    will_go_to_market = False


class SeventhTurn(TurnBase):
    turn_number = 7
    given_dice = {
        ResourceType.WOOD: 1,
        ResourceType.STONE: 2,
        ResourceType.LAND: 1,
        ResourceType.IRON: 1,
    }
    number_of_choices = 3
    will_go_to_market = True


@dataclass(frozen=True)
class Turn(object):
    turn_map = {
        1: FirstTurn,
        2: SecondTurn,
        3: ThirdTurn,
        4: FourthTurn,
        5: FifthTurn,
        6: SixthTurn,
        7: SeventhTurn,
    }

    def __new__(cls, turn_number: int) -> TurnBase:
        if turn_number in cls.turn_map:
            return cls.turn_map[turn_number]()
        raise InvalidTurnNumberError(f"Unknown Turn number {turn_number}")
