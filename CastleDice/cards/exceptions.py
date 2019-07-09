class InvalidCastleCardTypeError(Exception):
    """
    Raised when trying to instantiate a castle card but the type is not valid
    """


class InvalidMarketCardTypeError(Exception):
    """
    Raised when trying to instantiate a market card but the type is not valid
    """


class InvalidVillagerCardTypeError(Exception):
    """
    Raised when trying to instantiate a villager card but the type is not valid
    """
