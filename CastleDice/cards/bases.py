import abc

from CastleDice.common import DeckName
from CastleDice.common import PhaseType


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

    def __new__(cls, card_type, *args, **kwargs):
        """
        :param card_type:
        :param args:
        :param kwargs:
        :return BaseCard:
        """
        if not cls.card_map or not cls.card_lookup_error:
            raise NotImplementedError(
                "Both card_map and card_lookup_error must be set on child class")

        if card_type in cls.card_map:
            return cls.card_map[card_type](*args, **kwargs)

        raise cls.card_lookup_error()


# -- Mixins -- #
class CastleDeckMixin:
    @property
    def deck_type(self):
        return DeckName.CASTLE


class MarketDeckMixin:
    @property
    def deck_type(self):
        return DeckName.MARKET


class VillagerDeckMixin:
    @property
    def deck_type(self):
        return DeckName.VILLAGER


class NormalDiscardMixin:
    # TODO
    def discard(self):
        # remove this card from the player's hand, and put in discard pile
        raise NotImplementedError()


class NoDescriptionMixin:
    @property
    def description(self):
        return None


class NoBuildMixin:
    @property
    def build_cost(self):
        return ()


class NoScoreMixin:
    @property
    def victory_points(self):
        return 0

    def score(self):
        return


class NoOngoingMixin:
    @property
    def ongoing_phase(self):
        return None

    def use_ongoing(self):
        return

    def can_use_ongoing(self):
        return

    def has_ongoing_choice(self):
        return

    def reset_ongoing(self):
        return


class GatherPhaseMixin:
    @property
    def playable_phase(self):
        return PhaseType.GATHER


class BuildPhaseMixin:
    @property
    def playable_phase(self):
        return PhaseType.BUILD


class ChoosePhaseMixin:
    @property
    def playable_phase(self):
        return PhaseType.CHOOSE
