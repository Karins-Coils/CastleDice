from common.globals import WOOD, STONE, GOLD, LAND, IRON, \
    COW, CHICKEN, HORSE, PIG, BARBARIAN, BARN, JOAN

# Dice Faces based on resource
DICE_FACES = {
    WOOD: [
        (WOOD, 1),
        (WOOD, 1),
        (WOOD, 2),
        (WOOD, 3),
        (COW, 1),
        (BARBARIAN, 1)
    ],
    STONE: [
        (STONE, 1),
        (STONE, 1),
        (STONE, 2),
        (STONE, 2),
        (CHICKEN, 1),
        (BARBARIAN, 1)
    ],
    GOLD: [
        (GOLD, 1),
        (GOLD, 1),
        (GOLD, 1),
        (GOLD, 2),
        (HORSE, 1),
        (BARBARIAN, 1)
    ],
    LAND: [
        (LAND, 1),
        (LAND, 1),
        (LAND, 2),
        (PIG, 1),
        (PIG, 1),
        (BARBARIAN, 1)
    ],
    IRON: [
        (IRON, 1),
        (IRON, 2),
        (PIG, 1),
        (HORSE, 1),
        (CHICKEN, 1),
        (BARBARIAN, 1)
    ],
    JOAN: [
        (WOOD, 1),
        (STONE, 1),
        (GOLD, 1),
        (LAND, 1),
        (IRON, 1),
        (BARN, 1)
    ]
}

# Count of each type in the WorldPool
DICE_COUNT = {
    WOOD:  14,
    STONE: 14,
    GOLD:  13,
    LAND:  11,
    IRON:  11
}
