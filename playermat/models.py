from annoying.fields import JSONField
from django.contrib.auth.models import User
from django.db import models

from common.globals import GUARD, WORKER, BARBARIAN, ANIMAL_PREFERENCE, TURN


class PlayerMat(models.Model):
    player = models.ForeignKey(User)
    game = models.ForeignKey('game.Game')
    victory_points = models.PositiveSmallIntegerField(default=0)
    player_hand = JSONField(blank=True, null=True)
    player_merchant_hand = JSONField(blank=True, null=True)

    # turn based values - will be reset each turn
    player_order = models.PositiveSmallIntegerField(default=0)
    has_porkchopped = models.BooleanField(default=False)
    has_first_gathered = models.BooleanField(default=False)
    choice_dice = JSONField(blank=True, null=True)

    #-- counts for game --#
    # animals
    horses = models.PositiveSmallIntegerField(default=0)
    pigs = models.PositiveSmallIntegerField(default=0)
    cows = models.PositiveSmallIntegerField(default=0)
    chickens = models.PositiveSmallIntegerField(default=0)

    # resources
    wood = models.PositiveSmallIntegerField(default=0)
    stone = models.PositiveSmallIntegerField(default=0)
    gold = models.PositiveSmallIntegerField(default=0)
    land = models.PositiveSmallIntegerField(default=0)
    iron = models.PositiveSmallIntegerField(default=0)

    # villagers w/ only count
    merchants = models.PositiveSmallIntegerField(default=0)
    farmers = models.PositiveSmallIntegerField(default=0)

    def get_player_choice_extra_dice(self):
        # based on turn no, get number of 'extra' dice player will choose
        # to be added: logic to confirm if player has Royal Chambers etc
        return TURN[self.game.current_turn]['no_choices']


class PlayerMatResourcePeople(models.Model):
    TYPE_CHOICES = (
        (GUARD, GUARD),
        (WORKER, WORKER),
        (BARBARIAN, BARBARIAN)
    )

    player_mat = models.ForeignKey(PlayerMat)
    type = models.CharField(max_length='12', choices=TYPE_CHOICES)
    total = models.PositiveSmallIntegerField(default=0)
    wood = models.PositiveSmallIntegerField(default=0)
    stone = models.PositiveSmallIntegerField(default=0)
    gold = models.PositiveSmallIntegerField(default=0)
    land = models.PositiveSmallIntegerField(default=0)
    iron = models.PositiveSmallIntegerField(default=0)


class PlayerBuilt(models.Model):
    """
    The card that a player has built this game.
    """
    ANIMAL_CHOICES = [
        (name, name) for name in ANIMAL_PREFERENCE
    ]
    ANIMAL_CHOICES.append(('', ''))

    player_mat = models.ForeignKey(PlayerMat)
    card = models.CharField(max_length=52)
    count = models.PositiveSmallIntegerField(default=1)
    adds_animal = models.CharField(max_length=16, choices=ANIMAL_CHOICES)
