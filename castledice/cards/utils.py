from typing import Union

from castledice.common.constants import CastleCardType
from castledice.common.constants import MarketCardType
from castledice.common.constants import VillagerCardType
from .castle_cards import CastleCard
from .exceptions import InvalidDeckCardTypeError
from .market_cards import MarketCard
from .villager_cards import VillagerCard

__all__ = ["DeckCard"]


class DeckCard(object):
    """Given any card type, fetch its matching Card Class"""

    def __new__(
        cls,
        card_type: Union[CastleCardType, MarketCardType, VillagerCardType],
        *args,
        **kwargs
    ) -> Union[CastleCard, MarketCard, VillagerCard]:
        """
        :param card_type:
        :type: Union[CastleCardType, MarketCardType, VillagerCardType]
        :param args: any args to be passed to the custom card class
        :param kwargs: any kwargs to be passed to the custom card class
        :rtype: Union[CastleCard, MarketCard, VillagerCard]
        """
        if card_type in CastleCardType:
            cls = CastleCard

        elif card_type in MarketCardType:
            cls = MarketCard

        elif card_type in VillagerCardType:
            cls = VillagerCard

        else:
            raise InvalidDeckCardTypeError()

        return cls.card_map[card_type](*args, **kwargs)
