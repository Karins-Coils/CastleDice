from .constants import AnimalType
from .constants import ResourceType

__all__ = [
    'JOAN',
    'JOAN_GATHER_PREFERENCE',
    'PHASE',
]

# -- SOLO Play constants -- #
# not really a groupable type.  Joan is just... Joan...
JOAN = 'joan'

# Joan's Preferences, with first element being her first choice
JOAN_GATHER_PREFERENCE = ResourceType.values() + AnimalType.values()

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
