
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

#- Turn Settings
turn = {
    00: {
        'given_dice': [],
        'no_choices': 8
    },
    1: {
        'given_dice': [Wood, Wood, Stone, Stone, Gold],
        'no_choices': 2
    },
    2: {
        'given_dice': [Wood, Stone, Gold, Gold],
        'no_choices': 3
    },
    3: {
        'given_dice': [Wood, Wood, Wood, Stone, Gold],
        'no_choices': 3
    },
    4: {
        'given_dice': [Wood, Stone, Stone, Gold],
        'no_choices': 3
    },
    5: {
        'given_dice': [Wood, Stone, Gold, Land, Iron],
        'no_choices': 2
    },
    6: {
        'given_dice': [Wood, Wood, Gold, Iron],
        'no_choices': 3
    },
    7: {
        'given_dice': [Wood, Stone, Stone, Land, Iron],
        'no_choices': 3
    }
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