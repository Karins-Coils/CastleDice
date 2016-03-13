from django.db import models
from django.contrib.auth.models import User
from annoying.fields import JSONField

from CD_globals import GAME_DECK_NAMES


class Game(models.Model):
    current_player = models.ForeignKey(User, related_name='+')
    current_turn = models.PositiveSmallIntegerField(default=1)
    current_phase = models.PositiveSmallIntegerField(default=1)
    choice_dice = JSONField(blank=True)
    gather_dice = JSONField(blank=True)
    true_porkchop_used = models.BooleanField(default=False)


class GameDeck(models.Model):
    DECK_CHOICES = (
        (name, name)
        for name in GAME_DECK_NAMES
    )

    game = models.ManyToManyField(Game)
    deck = models.CharField(max_length=12, choices=DECK_CHOICES)
    draw_pile = models.CharField(max_length=500)
    discard_pile = models.CharField(max_length=500)
