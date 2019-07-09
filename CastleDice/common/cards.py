from .globals import WOOD, STONE, GOLD, LAND, \
    MERCHANT, WORKER, GUARD, FARMER

# - Card Names - #
# -- Villager Deck
SOLDIER = 'Soldier'
WISE_GRANDFATHER = 'Wise Grandfather'
KINGS_MESSENGER = "King's Messenger"


CASTLE_DECK_NAME = 'Castle'
CASTLE_DECK_CARDS = {
    # name: {
    #   'count' : 3,
    #   'phase' : 1,  #gather phase, build phase...
    #   #if build
    #   'resources' : { WOOD:1, STONE:2 }
    #   'victory_points' : #value the built item is worth
    #   'text' : # card text/description to make it easier for player to read
    # }

}

VILLAGER_DECK_NAME = 'Villager'
VILLAGER_DECK_CARDS = {
    # name: {
    #   'count' : 3,
    #   'phase' : 1, #gather phase, build phase...
    #   #if build
    #   'resources' : { WOOD:1, STONE:2 }
    #   'text' : # card text/description to make it easier for player to read
    # }

    MERCHANT: {
        'count': 7,
        'phase': 9,
        'resources': {
            GOLD: 3
        },
    },
    FARMER: {
        'count': 7,
        'phase': 9,
        'resources': {
            WOOD: 2,
            LAND: 1
        },
    },
    GUARD: {
        'count': 7,
        'phase': 9,
        'resources': {
            WOOD: 2
        },
    },
    WORKER: {
        'count': 8,
        'phase': 9,
        'resources': {
            WOOD: 1,
            STONE: 2
        },
    },
    WISE_GRANDFATHER: {
        'count': 4,
        'phase': 5,
        'text': "Play before you gather.  Gather one extra time this round.  "
                "After you've collected resources from both of your "
                "gatherings, roll those two dice back into the world pool."
    },
    KINGS_MESSENGER: {
        'count': 2,
        'phase': 5,
        'text': "Play instead of gathering.  The next player chooses a "
                "Villager type that you have room for.  You get that one for "
                "free!"
    },
    SOLDIER: {
        'count': 7,
        'phase': 4,
        'text': "Play before you gather.  Reroll all of your Barbarians into "
                "the world, keeping any that come up as Barbarians again."
    },


}


MARKET_DECK_NAME = 'Market'
MARKET_DECK_CARDS = {

}

GAME_DECK_NAMES = [CASTLE_DECK_NAME, VILLAGER_DECK_NAME, MARKET_DECK_NAME]
GAME_DECK_CARDS = {
    CASTLE_DECK_NAME: CASTLE_DECK_CARDS,
    VILLAGER_DECK_NAME: CASTLE_DECK_CARDS,
    MARKET_DECK_NAME: MARKET_DECK_CARDS
}

# build cards need to track possible usage during turn (Moat, Royal Chamber)
# or modify the player's stats

# 'effect' cards (squire, advisor, etc) can only be used during the matching
# phase, [match phase type, then allow usage]

# separate dict for effects?

# similar makeup for villager_deck_components