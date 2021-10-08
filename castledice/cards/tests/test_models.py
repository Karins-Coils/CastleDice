from castledice.common.constants import DeckName
from castledice.game.tests import utils

from ..decks import CastleDeck
from ..models import GameDeck
from .utils import serialize_pile


class TestGameDeck(utils.BaseGameTest):
    def test_get_deck__castle(self):
        game = self.create_one_player_game()
        castle_deck = CastleDeck()
        castle_deck.create_and_shuffle_draw_pile()
        game_deck = GameDeck(
            game=game,
            deck_type=DeckName.CASTLE.value,
            draw_pile=castle_deck.serialize_draw_pile(),
            discard_pile=[],
        )
        game_deck.save()

        retrieved_deck = game_deck.get_deck()
        assert serialize_pile(retrieved_deck._draw_pile) == serialize_pile(
            castle_deck._draw_pile
        )
        assert serialize_pile(retrieved_deck._discard_pile) == serialize_pile(
            castle_deck._discard_pile
        )
