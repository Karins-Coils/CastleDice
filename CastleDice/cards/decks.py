from typing import Dict
from typing import Sequence
from typing import Optional
from typing import Union

from CastleDice.common.constants import CastleCardType
from CastleDice.common.constants import DeckName
from CastleDice.common.constants import MarketCardType
from CastleDice.common.constants import VillagerCardType
from .castle_cards import CastleCard
from .market_cards import MarketCard
from .villager_cards import VillagerCard

__all__ = [
    'CastleDeck',
    'MarketDeck',
    'VillagerDeck',
]


_card_type = Union[CastleCard, MarketCard, VillagerCard]
_card_list_type = Sequence[_card_type]


class _Deck(object):
    # required on child class
    _deck_type: DeckName = None
    _deck_makeup: Dict[_card_type, int] = None

    # instance specific attributes
    _draw_pile: Optional[_card_list_type] = []
    _discard_pile: Optional[_card_list_type] = []

    def __init__(
            self,
            draw_pile: Optional[_card_list_type] = None,
            discard_pile: Optional[_card_list_type] = None):
        self._draw_pile = draw_pile
        self._discard_pile = discard_pile

    @property
    def type(self) -> DeckName:
        return self._deck_type


class CastleDeck(_Deck):
    _deck_type = DeckName.CASTLE
    _deck_makeup = {
        CastleCardType.ADVISOR: 2,
        CastleCardType.ALCHEMIST: 1,
        CastleCardType.DAUGHTER: 4,
        CastleCardType.DEEP_MOAT: 4,
        CastleCardType.GATE_HOUSE: 6,
        CastleCardType.GREAT_HALL: 4,
        CastleCardType.LOYAL_BROTHER: 3,
        CastleCardType.ROYAL_CHAMBERS: 6,
        CastleCardType.SQUIRE: 4,
        CastleCardType.STRONG_TOWER: 4,
        CastleCardType.TALL_KEEP: 3,
        CastleCardType.WALL_ANIMAL: 2,
        CastleCardType.WALL_FARMER: 1,
        CastleCardType.WALL_GUARD: 1,
        CastleCardType.WALL_MERCHANT: 1,
        CastleCardType.WALL_WORKER: 1,
    }


class MarketDeck(_Deck):
    _deck_type = DeckName.MARKET
    _deck_makeup = {
        MarketCardType.BARD: 3,
        MarketCardType.HUNGRY_BARBARIANS: 3,
        MarketCardType.JESTER: 3,
        MarketCardType.MAIDEN: 3,
        MarketCardType.SHEPHERD: 3,
        MarketCardType.VOLUNTEER: 3,
    }


class VillagerDeck(_Deck):
    _deck_type = DeckName.VILLAGER
    _deck_makeup = {
        VillagerCardType.FARMER: 7,
        VillagerCardType.GUARD: 7,
        VillagerCardType.KINGS_MESSENGER: 2,
        VillagerCardType.MERCHANT: 7,
        VillagerCardType.SOLDIER: 7,
        VillagerCardType.WISE_GRANDFATHER: 4,
        VillagerCardType.WORKER: 8,
    }
