
#- Die Faces & Values
# Resources
## Building Materials
Wood = 'wood'
Stone = 'stone'
Gold = 'gold'
Land = 'land'
Iron = 'iron'
## Animals
Horse = 'horse'
Pig = 'pig'
Cow = 'cow'
Chicken = 'chicken'
## Lone Barbarian
Barbarian = 'barbarian'

## Joan - solo play only
Joan = 'joan'
Barn = "barn"  # on Joan's Die
### Joan's Preferences, with first element being her first choice
ResourcePreference = [Iron, Land, Gold, Stone, Wood]
AnimalPreference = [Pig, Horse, Chicken, Cow]
GatherPreference = ResourcePreference + AnimalPreference

# Dice Faces based on resource
DiceFaces = {
    Wood: [
        (Wood, 1),
        (Wood, 1),
        (Wood, 2),
        (Wood, 3),
        (Cow, 1),
        (Barbarian, 1)
    ],
    Stone: [
        (Stone, 1),
        (Stone, 1),
        (Stone, 2),
        (Stone, 2),
        (Chicken, 1),
        (Barbarian, 1)
    ],
    Gold: [
        (Gold, 1),
        (Gold, 1),
        (Gold, 1),
        (Gold, 2),
        (Horse, 1),
        (Barbarian, 1)
    ],
    Land: [
        (Land, 1),
        (Land, 1),
        (Land, 2),
        (Pig, 1),
        (Pig, 1),
        (Barbarian, 1)
    ],
    Iron: [
        (Iron, 1),
        (Iron, 2),
        (Pig, 1),
        (Horse, 1),
        (Chicken, 1),
        (Barbarian, 1)
    ],
    Joan: [
        (Wood, 1),
        (Stone, 1),
        (Gold, 1),
        (Land, 1),
        (Iron, 1),
        (Barn, 1)
    ]
}

# Count of each type in the WorldPool
DiceCount = {
    Wood:  14,
    Stone: 14,
    Gold:  13,
    Land:  11,
    Iron:  11
}


#- Turn Settings
Turn = {
    00: {
        'given_dice': [],
        'no_choices': 8,
        'market': False
    },
    1: {
        'given_dice': [Wood, Wood, Stone, Stone, Gold],
        'no_choices': 2,
        'market': False
    },
    2: {
        'given_dice': [Wood, Stone, Gold, Gold],
        'no_choices': 3,
        'market': False
    },
    3: {
        'given_dice': [Wood, Wood, Wood, Stone, Gold],
        'no_choices': 3,
        'market': True
    },
    4: {
        'given_dice': [Wood, Stone, Stone, Gold],
        'no_choices': 3,
        'market': False
    },
    5: {
        'given_dice': [Wood, Stone, Gold, Land, Iron],
        'no_choices': 2,
        'market': True
    },
    6: {
        'given_dice': [Wood, Wood, Gold, Iron],
        'no_choices': 3,
        'market': False
    },
    7: {
        'given_dice': [Wood, Stone, Stone, Land, Iron],
        'no_choices': 3,
        'market': True
    }
}

#- Phase Descriptions
Phase = {
    1:  "Determine who goes first",  # Horse
    2:  "Choose & Draw cards in order (clockwise)",  # Draw phase, Chicken
    3:  "Players pick Choice dice (clockwise)",  # Choose, Cow
    4:  "All dice are rolled; World Formed",  # World Pool
    5:  "Gather resources in order until gone (clockwise)",  # Gather, Pig
    6:  "Go to Market (clockwise)",  # Market
    7:  "Workers Produce",  # Workers
    8:  "Merchants Work",  # Merchants
    9:  "Build",  # Build
    10: "Barbarians Raid"  # Barbarians
}

#easier/cleaner to have the dict be turn['given_dice'][#] ?
# logically no.  more confusing, to me at least.  because I need all
# info for that turn, and may not know what exactly i need until I
# have the info.  better to have it grouped by turn #

castle_deck_components = {
    # name: {
    #   'count' : x,
    #   'type' : #gather phase, build phase...
    #   #if build
    #   'resources' : [(Wood, 2), (Stone, 1)]
    #   'victory_points' : #value the built item is worth
    #   'text' : # card text/description to make it easier for player to read
    # }

}
# build cards need to track possible usage during turn (Moat, Royal Chamber) or modify the player's stats

# 'effect' cards (squire, advisor, etc) can only be used during the matching phase, [match phase type, then allow usage]

# separate dict for effects?

# similar makeup for villager_deck_components