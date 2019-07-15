from CastleDice.common.constants import MarketCardType
from CastleDice.common.constants import PhaseType
from CastleDice.common.constants import SpecialPhaseType
from .card_bases import BaseCard
from .card_bases import BuildPhaseMixin
from .card_bases import CardLookupBase
from .card_bases import GatherPhaseMixin
from .card_bases import MarketDeckMixin
from .card_bases import NoBuildMixin
from .card_bases import NoOngoingMixin
from .card_bases import NoScoreMixin
from .card_bases import NormalDiscardMixin
from .exceptions import InvalidMarketCardTypeError


class Bard(
    NoBuildMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    MarketDeckMixin,
    BaseCard
):
    _constant = MarketCardType.BARD

    playable_phase = SpecialPhaseType.END_GAME
    victory_points = 1
    description = "Reveal this card at the end of the game.  It gives 1 Victory Point"

    def is_playable(self):
        # if current phase is playable phase return True
        raise NotImplementedError()

    def play(self):
        # confirm is_playable
        # add to built cards
        raise NotImplementedError()

    def score(self):
        raise NotImplementedError()


class HungryBarbarians(
    GatherPhaseMixin,
    NoBuildMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    MarketDeckMixin,
    BaseCard
):
    _constant = MarketCardType.HUNGRY_BARBARIANS

    playable_phase = SpecialPhaseType.FIRST_GATHER
    description = "Play before your first gather. Choose two types of Animals.  All players " \
                  "must discard all those two types of Animals."

    def is_playable(self):
        # if current phase is playable phase return True
        # also confirm is the FIRST gather only
        raise NotImplementedError()

    def play(self):
        # confirm is_playable
        # have player choose two types of animals
        # remove those animals from all players' mats
        raise NotImplementedError()


class Jester(
    GatherPhaseMixin,
    NoBuildMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    MarketDeckMixin,
    BaseCard
):
    _constant = MarketCardType.JESTER

    description = "Play before you gather. All players re-roll their Barbarians. You may give " \
                  "any barbarians you roll to another player."

    def is_playable(self):
        # if current phase is playable phase return True
        # also confirm is the FIRST gather only
        raise NotImplementedError()

    def play(self):
        # confirm is_playable
        # re-roll all barbarians on the table
        # if other players roll barbarians a second time, they keep them
        # player of this card can give any re-rolled barbarians to another
        # rolled resources added to the world pool
        raise NotImplementedError()


class Maiden(
    GatherPhaseMixin,
    NoBuildMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    MarketDeckMixin,
    BaseCard
):
    _constant = MarketCardType.MAIDEN

    description = "Play before you gather. Discard any number of Castle and/or Village cards to " \
                  "draw the same number from either deck(s)."

    def is_playable(self):
        # if current phase is playable phase return True
        raise NotImplementedError()

    def play(self):
        # confirm is_playable
        # ask player to choose Castle/Village cards from their hand for discard
        # allow player to draw that many cards again from either deck(s)
        raise NotImplementedError()


class Shepherd(
    NoBuildMixin,
    NoOngoingMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    MarketDeckMixin,
    BaseCard
):
    _constant = MarketCardType.SHEPHERD

    playable_phase = SpecialPhaseType.FIRST_GATHER
    description = "Play before your first gather. Choose one type of Animal. All other players " \
                  "give you all of that Animal type they have."

    def is_playable(self):
        # if current phase is playable phase return True
        # confirm FIRST GATHER
        raise NotImplementedError()

    def play(self):
        # confirm is_playable
        # have player choose an animal
        # all other players give that type of animal to this player
        raise NotImplementedError()


class Volunteer(
    BuildPhaseMixin,
    NoBuildMixin,
    NormalDiscardMixin,
    NoScoreMixin,
    MarketDeckMixin,
    BaseCard
):
    _constant = MarketCardType.VOLUNTEER

    ongoing_phase = SpecialPhaseType.ANY
    description = "Play during your Build phase. This card stays in play and counts as an extra " \
                  "Wall when other cards reference the number of Walls you have"

    def is_playable(self):
        # if current phase is playable phase return True
        raise NotImplementedError()

    def play(self):
        # confirm is_playable
        # add to built things
        raise NotImplementedError()

    def can_use_ongoing(self):
        raise NotImplementedError()

    def has_ongoing_choice(self):
        raise NotImplementedError()

    def reset_ongoing(self):
        # card ongoing state never needs to be reset -- always active
        return None

    def use_ongoing(self):
        # treat as a wall...
        raise NotImplementedError()


class MarketCard(CardLookupBase):
    card_map = {
        MarketCardType.BARD: Bard,
        MarketCardType.HUNGRY_BARBARIANS: HungryBarbarians,
        MarketCardType.JESTER: Jester,
        MarketCardType.MAIDEN: Maiden,
        MarketCardType.SHEPHERD: Shepherd,
        MarketCardType.VOLUNTEER: Volunteer,
    }
    card_lookup_error = InvalidMarketCardTypeError
