
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
