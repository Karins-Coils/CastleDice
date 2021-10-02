# -- Die Faces & Values -- #
# - Resources - #
# Building Materials
WOOD = "wood"
STONE = "stone"
GOLD = "gold"
LAND = "land"
IRON = "iron"
# Animals
HORSE = "horse"
PIG = "pig"
COW = "cow"
CHICKEN = "chicken"
# Lone Barbarian
BARBARIAN = "barbarian"
# Villagers
WORKER = "worker"
GUARD = "guard"
FARMER = "farmer"
MERCHANT = "merchant"

# Joan - solo play only
JOAN = "joan"
BARN = "barn"  # on Joan's Die
# Joan's Preferences, with first element being her first choice
RESOURCE_PREFERENCE = (IRON, LAND, GOLD, STONE, WOOD)
ANIMAL_PREFERENCE = (PIG, HORSE, CHICKEN, COW)
GATHER_PREFERENCE = RESOURCE_PREFERENCE + ANIMAL_PREFERENCE

# ----- Convert to Enum/objects
# -- Turn Settings -- #
TURN = {
    00: {"given_dice": [], "no_choices": 8, "market": False},
    1: {
        "given_dice": {WOOD: 2, STONE: 2, GOLD: 1},  # [WOOD, WOOD, STONE, STONE, GOLD],
        "no_choices": 2,
        "market": False,
    },
    2: {
        "given_dice": {WOOD: 1, STONE: 1, GOLD: 2},  # [WOOD, STONE, GOLD, GOLD],
        "no_choices": 3,
        "market": False,
    },
    3: {
        "given_dice": {WOOD: 3, STONE: 1, GOLD: 1},  # [WOOD, WOOD, WOOD, STONE, GOLD],
        "no_choices": 3,
        "market": True,
    },
    4: {
        "given_dice": {WOOD: 1, STONE: 2, GOLD: 1},  # [WOOD, STONE, STONE, GOLD],
        "no_choices": 3,
        "market": False,
    },
    5: {
        "given_dice": {
            WOOD: 1,
            STONE: 1,
            GOLD: 1,
            LAND: 1,
            IRON: 1,
        },  # [WOOD, STONE, GOLD, LAND, IRON],
        "no_choices": 2,
        "market": True,
    },
    6: {
        "given_dice": {WOOD: 2, GOLD: 2, IRON: 2},  # [WOOD, WOOD, GOLD, IRON],
        "no_choices": 3,
        "market": False,
    },
    7: {
        "given_dice": {
            WOOD: 1,
            STONE: 2,
            LAND: 1,
            IRON: 1,
        },  # [WOOD, STONE, STONE, LAND, IRON],
        "no_choices": 3,
        "market": True,
    },
}

# -- Phase Descriptions -- #
PHASE = {
    # Horse
    1: ("Player Order", "Determine who goes first"),
    # Draw phase, Chicken
    2: ("Choose Cards", "Choose & Draw cards in order (clockwise)"),
    # Choose, Cow
    3: ("Choose Dice", "Players pick Choice dice (clockwise)"),
    # World Pool
    4: ("Roll Dice", "All dice are rolled; World Formed"),
    # Gather, Pig
    5: ("Gather Dice", "Gather resources in order until gone (clockwise)"),
    # Market
    6: ("Go to Market", "Go to Market (clockwise)"),
    # Workers
    7: ("Workers Produce", "Workers Produce"),
    # Merchants
    8: ("Merchants Trade", "Merchants Trade"),
    # Build
    9: ("Build", "Build"),
    # Barbarians
    10: ("Barbarians Raid", "Barbarians Raid"),
}

# easier/cleaner to have the dict be turn['given_dice'][#] ?
# logically no.  more confusing, to me at least.  because I need all
# info for that turn, and may not know what exactly i need until I
# have the info.  better to have it grouped by turn #
