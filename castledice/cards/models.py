from typing import Union

from django.contrib.postgres.fields import ArrayField
from django.db import models

from castledice.common.constants import DeckName

from .decks import CastleDeck, MarketDeck, VillagerDeck
from .exceptions import InvalidDeckTypeError


class GameDeck(models.Model):
    game = models.ForeignKey(to="game.Game", on_delete=models.CASCADE)
    deck_type = models.CharField(max_length=10, choices=DeckName.django_choices())
    draw_pile = ArrayField(models.TextField())
    discard_pile = ArrayField(models.TextField())

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("game_id", "deck_type"), name="unique deck per game"
            )
        ]

    def get_deck(self) -> Union[CastleDeck, MarketDeck, VillagerDeck]:
        """Convert this GameDeck to a Deck object"""
        if self.deck_type == DeckName.CASTLE:
            deck_class = CastleDeck
        elif self.deck_type == DeckName.MARKET:
            deck_class = MarketDeck
        elif self.deck_type == DeckName.VILLAGER:
            deck_class = VillagerDeck
        else:
            raise InvalidDeckTypeError("Unknown deck class for %s" % self.deck_type)

        return deck_class(draw_pile=self.draw_pile, discard_pile=self.discard_pile)
