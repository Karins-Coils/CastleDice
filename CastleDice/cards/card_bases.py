import abc
from typing import Union

from CastleDice.common.constants import CastleCardType
from CastleDice.common.constants import DeckName
from CastleDice.common.constants import MarketCardType
from CastleDice.common.constants import PhaseType
from CastleDice.common.constants import VillagerCardType


class ResourceCost(object):
    _resource = None
    _amount = None

    def __init__(self, resource, amount):
        self._resource = resource
        self._amount = amount

    @property
    def resource(self):
        """
        :return constants.Resources:
        """
        return self._resource

    @property
    def amount(self):
        """
        :return int:
        """
        return self._amount


class BaseCard(metaclass=abc.ABCMeta):
    # expects constants.VillagerCard, constants.CastleCard, constants.MarketCard, etc
    _constant = None

    # --- read only public class attributes --- #
    @property
    def card_id(self):
        """
        Used for serialization purposes

        :return str:
        """
        return self._constant.value

    @property
    def name(self):
        """
        Human readable name of card

        :return str:
        """

        # convert name from snake_case to spaces and title case
        return self._constant.name.replace('_', ' ').title()

    # TODO
    # @property
    # @abc.abstractmethod
    # def image(self):
    #     """Image for card"""

    @property
    @abc.abstractmethod
    def description(self):
        """Human readable description of card

        :return str:
        """

    @property
    @abc.abstractmethod
    def playable_phase(self):
        """
        Phase in which this card can be used - will be used as a precondition check in
        self.is_playable

        :return common.Phases:
        """

    @property
    @abc.abstractmethod
    def ongoing_phase(self):
        """
        Phase in which any ongoing special effects can be enacted

        :return common.Phases:
        """

    @property
    @abc.abstractmethod
    def deck_type(self):
        """
        Deck in which this card belongs - Castle, Villager, Market, etc

        :return common.DeckNames:
        """

    @property
    @abc.abstractmethod
    def victory_points(self):
        """
        Victory Points this card gives, if any - will be used when calling self.score

        :return int:
        """

    @property
    @abc.abstractmethod
    def build_cost(self):
        """
        List of resources required to build this card

        :return tuple(ResourceCost):
        """

    # --- public methods --- #
    def serialize(self) -> str:
        return self.card_id

    @abc.abstractmethod
    def is_playable(self):
        """
        Check if this card can be played by looking at all pre-conditions
        """

    @abc.abstractmethod
    def play(self):
        """
        Play this card and trigger any events/effects as a result
        -- Should call to is_playable first to verify pre-conditions met
        """

    @abc.abstractmethod
    def score(self):
        """
        (optional)
        When scoring at the end, this will calculate the base + any special additions.
        * Not all cards will have this method *
        """

    @abc.abstractmethod
    def discard(self):
        """
        Triggered by cards without an ongoing
        """

    @abc.abstractmethod
    def use_ongoing(self):
        """
        Enact ongoing effects
        """

    @abc.abstractmethod
    def can_use_ongoing(self):
        """
        Checks preconditions on ongoing effects
        """

    @abc.abstractmethod
    def has_ongoing_choice(self):
        """
        Some ongoing effects give the user a choice of when they want to use it
        """

    @abc.abstractmethod
    def reset_ongoing(self):
        """
        An ongoing can usually only be used once per turn.  This will reset the internal state
        """


class CardLookupBase(object):
    card_map = {}  # to be filled in by subclass
    card_lookup_error = None  # to be customized in each subclass

    def __new__(cls,
                card_type: Union[MarketCardType, VillagerCardType, CastleCardType, str],
                *args,
                **kwargs) -> BaseCard:
        if not cls.card_map or not cls.card_lookup_error:
            raise NotImplementedError(
                "Both card_map and card_lookup_error must be set on child class")

        if card_type in cls.card_map:
            return cls.card_map[card_type](*args, **kwargs)

        raise cls.card_lookup_error()


# -- Mixins -- #
class CastleDeckMixin:
    deck_type = DeckName.CASTLE


class MarketDeckMixin:
    deck_type = DeckName.MARKET


class VillagerDeckMixin:
    deck_type = DeckName.VILLAGER


class NormalDiscardMixin:
    # TODO
    def discard(self):
        # remove this card from the player's hand, and put in discard pile
        raise NotImplementedError()


class NoDescriptionMixin:
    description = None


class NoBuildMixin:
    build_cost = tuple()


class NoScoreMixin:
    victory_points = 0

    def score(self):
        return


class NoOngoingMixin:
    ongoing_phase = None

    def use_ongoing(self):
        return

    def can_use_ongoing(self):
        return

    def has_ongoing_choice(self):
        return

    def reset_ongoing(self):
        return


class GatherPhaseMixin:
    playable_phase = PhaseType.GATHER


class BuildPhaseMixin:
    playable_phase = PhaseType.BUILD


class ChoosePhaseMixin:
    playable_phase = PhaseType.CHOOSE
