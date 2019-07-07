import abc

from ..common import DeckNames
from ..common import Phases


class BaseCard(metaclass=abc.ABCMeta):
    # --- read only public class attributes --- #
    @property
    @abc.abstractmethod
    def card_id(self):
        """Used for serialization purposes"""

    @property
    @abc.abstractmethod
    def name(self):
        """Human readable name of card"""

    # TODO
    # @property
    # @abc.abstractmethod
    # def image(self):
    #     """Image for card"""

    @property
    @abc.abstractmethod
    def description(self):
        """Human readable description of card"""

    @property
    @abc.abstractmethod
    def playable_phase(self):
        """
        Phase in which this card can be used - will be used as a precondition check in
        self.is_playable
        """

    @property
    @abc.abstractmethod
    def ongoing_phase(self):
        """
        Phase in which any ongoing special effects can be enacted
        """

    @property
    @abc.abstractmethod
    def deck_type(self):
        """Deck in which this card belongs - Castle, Villager, Market, etc"""

    @property
    @abc.abstractmethod
    def victory_points(self):
        """
        (optional)
        Victory Points this card gives, if any - will be used when calling self.score
        """

    @property
    @abc.abstractmethod
    def build_cost(self):
        """
        (optional)
        List of resources required to build this card
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


# -- Mixins -- #
class CastleDeckMixin:
    @property
    def deck_type(self):
        return DeckNames.CASTLE


class MarketDeckMixin:
    @property
    def deck_type(self):
        return DeckNames.MARKET


class VillagerDeckMixin:
    @property
    def deck_type(self):
        return DeckNames.VILLAGER


class NormalDiscard:
    # TODO
    def discard(self):
        # remove this card from the player's hand, and put in discard pile
        pass


class NoBuildMixin:
    @property
    def build_cost(self):
        return []


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
        return Phases.GATHER


class BuildPhaseMixin:
    @property
    def playable_phase(self):
        return Phases.BUILD


class ChoosePhaseMixin:
    @property
    def playable_phase(self):
        return Phases.CHOOSE
