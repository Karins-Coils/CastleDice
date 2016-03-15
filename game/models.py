from collections import defaultdict

from annoying.fields import JSONField
from django.contrib.auth.models import User
from django.db import models

from common.dice import DICE_COUNT
from common.cards import GAME_DECK_NAMES
from common.globals import TURN


class Game(models.Model):
    is_solo_game = models.BooleanField(default=False)
    current_player = models.ForeignKey(User,
                                       related_name='+',
                                       blank=True,
                                       null=True)
    current_turn = models.PositiveSmallIntegerField(default=1)
    current_phase = models.PositiveSmallIntegerField(default=1)
    choice_dice = JSONField(blank=True, null=True)
    gather_dice = JSONField(blank=True, null=True)
    true_porkchop_used = models.BooleanField(default=False)

    def setup_choice_dice_for_turn(self):
        player_count = self.playermat_set.count()
        given_dice = TURN[self.current_turn]['given_dice']

        # setup base choice die for all players
        for playermat in self.playermat_set.all():
            playermat.choice_dice = given_dice
            playermat.save()

        # create choice pool from remaining dice
        # get count for this resource, multiply by players
        # subtract the already claimed dice from the remaining pool
        total_dice = {
            resource: value - (given_dice.get(resource, 0) * player_count)
            for resource, value in DICE_COUNT.iteritems()
        }
        self.choice_dice = total_dice
        self.save()


class GameDeck(models.Model):
    DECK_CHOICES = (
        (name, name)
        for name in GAME_DECK_NAMES
    )

    game = models.ManyToManyField(Game)
    deck = models.CharField(max_length=12, choices=DECK_CHOICES)
    draw_pile = models.CharField(max_length=500)
    discard_pile = models.CharField(max_length=500)
