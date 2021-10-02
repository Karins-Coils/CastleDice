from enum import IntEnum, unique

from .named_constants import Constants

__all__ = [
    "AnimalType",
    "CastleCardType",
    "DeckName",
    "DieFace",
    "GameConstants",
    "JoanDieFace",
    "MarketCardType",
    "PhaseType",
    "ResourceType",
    "SpecialPhaseType",
    "TurnType",
    "VillagerCardType",
    "VillagerType",
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

# Set values, easy to reference
class GameConstants(Constants):
    MAX_RESOURCES = 10  # only 10 of each resources allowed


# Sorted by Resource Preference Gathering - especially Joan
class ResourceType(Constants):
    WOOD = _Globals.WOOD.value
    STONE = _Globals.STONE.value
    GOLD = _Globals.GOLD.value
    LAND = _Globals.LAND.value
    IRON = _Globals.IRON.value


# Sorted by Animal Preference Gathering - especially Joan
class AnimalType(Constants):
    PIG = _Globals.PIG.value
    HORSE = _Globals.HORSE.value
    CHICKEN = _Globals.CHICKEN.value
    COW = _Globals.COW.value


class VillagerType(Constants):
    WORKER = _Globals.WORKER.value
    GUARD = _Globals.GUARD.value
    FARMER = _Globals.FARMER.value
    MERCHANT = _Globals.MERCHANT.value


class DieFace(Constants):
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


class JoanDieFace(Constants):
    WOOD = _Globals.WOOD.value
    STONE = _Globals.STONE.value
    GOLD = _Globals.GOLD.value
    LAND = _Globals.LAND.value
    IRON = _Globals.IRON.value

    BARN = _Globals.BARN.value


class DeckName(Constants):
    CASTLE = _Globals.CASTLE.value
    MARKET = _Globals.MARKET.value
    VILLAGER = _Globals.VILLAGER.value


class CastleCardType(Constants):
    ADVISOR = "C01"
    ALCHEMIST = "C02"
    DAUGHTER = "C03"
    DEEP_MOAT = "C04"
    GATE_HOUSE = "C05"
    GREAT_HALL = "C06"
    LOYAL_BROTHER = "C07"
    ROYAL_CHAMBERS = "C08"
    SQUIRE = "C09"
    STRONG_TOWER = "C10"
    TALL_KEEP = "C11"
    WALL_ANIMAL = "C12"
    WALL_FARMER = "C13"
    WALL_GUARD = "C14"
    WALL_MERCHANT = "C15"
    WALL_WORKER = "C16"


class MarketCardType(Constants):
    BARD = "M01"
    HUNGRY_BARBARIANS = "M02"
    JESTER = "M03"
    MAIDEN = "M04"
    SHEPHERD = "M05"
    VOLUNTEER = "M06"


class VillagerCardType(Constants):
    """
    These attributes do not stem from _Globals, as their explicit strings are needed for
    ordering, display and lookup
    """

    FARMER = "V01"
    GUARD = "V02"
    KINGS_MESSENGER = "V03"
    MERCHANT = "V04"
    SOLDIER = "V05"
    WISE_GRANDFATHER = "V06"
    WORKER = "V07"


class PhaseType(Constants):
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


class SpecialPhaseType(Constants):
    FIRST_GATHER = 40
    ANY = 100
    END_GAME = 200


class TurnType(Constants):
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
