from annoying.fields import JSONField
from django.contrib.auth.models import User
from django.db import models

from common.globals import GUARD, WORKER, BARBARIAN, \
    ANIMAL_PREFERENCE, RESOURCE_PREFERENCE, TURN
from die.dieClass import Die


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
    has_farmered = models.BooleanField(default=False)
    choice_dice = JSONField(blank=True, null=True)

    # -- counts for game -- #
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

    def add_resource(self, die_tuple):
        """
        Match the resource to the column and add to value
        :param tuple die_tuple: (resource, count) ex: (WOOD, 2)
        :return:
        """
        self.__dict__[die_tuple[0]] += die_tuple[1]
        self.save()

    def remove_resource(self, resource, count=1):
        """
        Match resource to column and remove count, default 1
        :param resource:
        :param count:
        :return:
        """
        self.__dict__[resource] -= count
        self.save()

    def reset_turn_based(self):
        self.has_porkchopped = False
        self.has_first_gathered = False
        self.has_farmered = False
        self.choice_dice = False
        self.save()

        try:
            barbarians = self.playermatresourcepeople_set.get(type=BARBARIAN)
            barbarians.clear_all()
        except self.DoesNotExist:
            # no barbarians to clear
            pass

    def current_hand_size(self):
        return len(self.player_hand)

    def update_rolled_dice(self, dice_list):
        # take in a list of dice, if barbarian, add to playerResourcePeople
        # if regular resource, add to game world pool
        # for die in dice_list:
        #     if
        pass

    def has_max_animal(self, animal):
        """
        Given an animal, query the related players.  If any have value
        greater than or equal to current player, returns False.  Else True.
        :param str animal: CastleDice constant
        :return: whether this player has the most of that animal
        :rtype: bool
        """
        kwargs = {animal+"__gte": self.__dict__[animal]}
        if self.game.playermat_set.filter(**kwargs).exclude(id=self.id):
            return False
        return True

    def go_to_market(self, count=1, max=False):

        # can go to market as many times as the least animal
        max_market = min(self.cows, self.chickens, self.horses, self.pigs)
        if max_market == 0:
            return

        # go to market for count, or max
        pass

    def roll_choice_dice(self):
        rolled_dice = Die.roll_die_list(self.choice_dice)

        for resource_type, die_face_list in rolled_dice.items():
            for die_face in die_face_list:
                if Die.is_barbarian(die_face):
                    barbarians = self.playermatresourcepeople_set.get_or_create(
                        type=BARBARIAN)[0]
                    barbarians.add_resource(resource_type)

        return rolled_dice


class JoanPlayerMat(PlayerMat):
    resource_choices = (
        (die, die) for die in list(RESOURCE_PREFERENCE) + [None]
    )

    # turn based values - will be reset each turn
    primary_resource = models.CharField(max_length=12,
                                        blank=True,
                                        null=True,
                                        choices=resource_choices)

    def reset_turn_based(self):
        self.primary_resource = None
        self.save()
        super(JoanPlayerMat, self).reset_turn_based()


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

    class Meta:
        unique_together = (("player_mat", "type"),)

    def clear_all(self):
        # should only be done on barbarian rows
        for resource in list(RESOURCE_PREFERENCE) + ['total']:
            self.__dict__[resource] = 0
        self.save()

    def remove_resource(self, resource, count=1):
        self.__dict__[resource] -= count
        self.total -= count
        self.save()

    def add_resource(self, resource, count=1):
        self.__dict__[resource] += count
        self.total += count
        self.save()


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
