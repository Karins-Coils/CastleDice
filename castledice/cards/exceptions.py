class InvalidDeckCardTypeError(Exception):
    """
    Raised when trying to instantiate a card, and can not identify which deck it belongs
    """


class InvalidCastleCardTypeError(InvalidDeckCardTypeError):
    """
    Raised when trying to instantiate a castle card but the type is not valid
    """


class InvalidMarketCardTypeError(InvalidDeckCardTypeError):
    """
    Raised when trying to instantiate a market card but the type is not valid
    """


class InvalidVillagerCardTypeError(InvalidDeckCardTypeError):
    """
    Raised when trying to instantiate a villager card but the type is not valid
    """


class InvalidDeckTypeError(Exception):
    """
    When a DeckName does match expected values
    """
