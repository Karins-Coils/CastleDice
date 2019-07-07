from enum import IntEnum
from enum import unique

from .named_constants import Constants

__all__ = [
    'Animals',
    'DeckNames',
    'DieFaces',
    'JoanDieFaces',
    'Phases',
    'Resources',
    'Turns',
    'VillagerCards',
    'Villagers',
    'JOAN',
    'JOAN_GATHER_PREFERENCE',
    'PHASE',
]


# -- Non-importable, only for use in this file -- #
@unique  # unique here guarantees that no two keys share the same value in this file
class _Globals(IntEnum):
    # Building Resources
    WOOD = 0
    STONE = 1
    GOLD = 2
    LAND = 3
    IRON = 4

    # Animals
    PIG = 5
    HORSE = 6
    CHICKEN = 7
    COW = 8

    # Lone Barbarian
    BARBARIAN = 9

    # Villagers
    WORKER = 50
    GUARD = 51
    FARMER = 52
    MERCHANT = 53

    # Decks
    CASTLE = 100
    MARKET = 101
    VILLAGER = 102

    # Joan - solo play only
    JOAN = 200
    BARN = 201  # on Joan's Die


# -- importable classes, used for many things -- #

# Sorted by Resource Preference Gathering - especially Joan
class Resources(Constants):
    WOOD = _Globals.WOOD.value
    STONE = _Globals.STONE.value
    GOLD = _Globals.GOLD.value
    LAND = _Globals.LAND.value
    IRON = _Globals.IRON.value


# Sorted by Animal Preference Gathering - especially Joan
class Animals(Constants):
    PIG = _Globals.PIG.value
    HORSE = _Globals.HORSE.value
    CHICKEN = _Globals.CHICKEN.value
    COW = _Globals.COW.value


class Villagers(Constants):
    WORKER = _Globals.WORKER.value
    GUARD = _Globals.GUARD.value
    FARMER = _Globals.FARMER.value
    MERCHANT = _Globals.MERCHANT.value


class DieFaces(Constants):
    WOOD = _Globals.WOOD.value
    STONE = _Globals.STONE.value
    GOLD = _Globals.GOLD.value
    LAND = _Globals.LAND.value
    IRON = _Globals.IRON.value

    PIG = _Globals.PIG.value
    HORSE = _Globals.HORSE.value
    CHICKEN = _Globals.CHICKEN.value
    COW = _Globals.COW.value

    BARBARIAN = _Globals.BARBARIAN.value


class JoanDieFaces(Constants):
    WOOD = _Globals.WOOD.value
    STONE = _Globals.STONE.value
    GOLD = _Globals.GOLD.value
    LAND = _Globals.LAND.value
    IRON = _Globals.IRON.value

    BARN = _Globals.BARN.value


class DeckNames(Constants):
    CASTLE = _Globals.CASTLE.value
    MARKET = _Globals.MARKET.value
    VILLAGER = _Globals.VILLAGER.value


class VillagerCards(Constants):
    """
    These attributes do not stem from _Globals, as their explicit strings are needed for
    ordering, display and lookup
    """
    SOLDIER = "V01"
    WORKER = "V02"
    FARMER = "V03"
    GUARD = "V04"
    MERCHANT = "V05"
    KINGS_MESSENGER = "V06"
    WISE_GRANDFATHER = "V07"


class Phases(Constants):
    """
    These attributes do not stem from _Globals, as their explicit numbers are needed for
    ordering and display
    """
    ORDER = 1
    DRAW = 2
    CHOOSE = 3
    ROLL = 4
    GATHER = 5
    MARKET = 6
    WORKERS = 7
    MERCHANTS = 8
    BUILD = 9
    BARBARIANS = 10


class Turns(Constants):
    """
    These attributes do not stem from _Globals, as their explicit numbers are needed for
    ordering and display
    """
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    SIXTH = 6
    SEVENTH = 7


# -- SOLO Play constants -- #
# not really a groupable type.  Joan is just... Joan...
JOAN = 'joan'

# Joan's Preferences, with first element being her first choice
JOAN_GATHER_PREFERENCE = Resources.values() + Animals.values()


# -- Game Data -- #
PHASE = (
    # skip zero index for ease of calculation
    (),
    # 1 - Horse
    ("Player Order", "Determine who goes first"),
    # 2 - Draw phase, Chicken
    ("Choose Cards", "Choose & Draw cards in order (clockwise)"),
    # 3 - Choose, Cow
    ("Choose Dice", "Players pick Choice dice (clockwise)"),
    # 4 - World Pool
    ("Roll Dice", "All dice are rolled; World Formed"),
    # 5 - Gather, Pig
    ("Gather Dice", "Gather resources in order until gone (clockwise)"),
    # 6 - Market
    ("Go to Market", "Go to Market (clockwise)"),
    # 7 - Workers
    ("Workers Produce", "Workers Produce"),
    # 8 - Merchants
    ("Merchants Trade", "Merchants Trade"),
    # 9 - Build
    ("Build", "Build"),
    # 10 -Barbarians
    ("Barbarians Raid", "Barbarians Raid"),
)
