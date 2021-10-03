from typing import Optional

from annoying.fields import JSONField
from django.conf import settings
from django.db import models

from castledice.common.constants import GameConstants, ResourceType, VillagerType
from castledice.common.globals import ANIMAL_PREFERENCE, BARBARIAN, RESOURCE_PREFERENCE
from castledice.die.dieClass import Die
from castledice.game.turns import Turn

from .exceptions import (
    InvalidResourceForVillagerError,
    MissingGuardResourceError,
    NoMoreOfVillagerError,
    VillagerMaxedOutError,
    WorkersFullError,
)


class PlayerMat(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey("game.Game", on_delete=models.CASCADE)
    victory_points = models.PositiveSmallIntegerField(default=0)
    player_hand = JSONField(blank=True, null=True)
    player_merchant_hand = JSONField(blank=True, null=True)

    # turn based values - will be reset each turn
    player_order = models.PositiveSmallIntegerField(default=0)
    has_porkchopped = models.BooleanField(default=False)
    has_first_gathered = models.BooleanField(default=False)
    has_farmered = models.BooleanField(default=False)
    choice_dice = JSONField(blank=True, null=True, default=[])

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

    # will be reset after each turn
    barbarians = models.PositiveSmallIntegerField(default=0)

    def get_player_choice_extra_dice(self):
        # based on turn no, get number of 'extra' dice player will choose
        # TODO: logic to confirm if player has Royal Chambers etc
        return Turn(self.game.current_turn.turn_no).number_of_choices

    def add_resource(self, resource: ResourceType, add_amount: int = 1):
        """
        Match the resource to the column and add amount to value

        :param resource:
        :type: ResourceType
        :param add_amount:
        :type: int
        """
        attr_name = resource.name.lower()
        current_amount = self.__getattribute__(attr_name)
        # adding more than the allowed max
        new_amount = min(current_amount + add_amount, GameConstants.MAX_RESOURCES)

        self.__setattr__(attr_name, new_amount)
        self.save()

    def remove_resource(self, resource, remove_amount=1):
        """
        Match resource to column and remove count, default 1
        :param resource:
        :type resource: ResourceType
        :param remove_amount:
        :type remove_amount: int
        """
        attr_name = resource.name.lower()
        current_amount = self.__getattribute__(attr_name)
        # cannot have a negative amount of a resource
        new_amount = max(current_amount - remove_amount, 0)

        self.__setattr__(attr_name, new_amount)
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
        :param str animal: castledice constant
        :return: whether this player has the most of that animal
        :rtype: bool
        """
        kwargs = {animal + "__gte": self.__dict__[animal]}
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
                        type=BARBARIAN
                    )[0]
                    barbarians.add_resource(resource_type)

        self.choice_dice = []
        self.save()
        return rolled_dice


class JoanPlayerMat(PlayerMat):
    resource_choices = ((die, die) for die in list(RESOURCE_PREFERENCE) + [None])

    # turn based values - will be reset each turn
    primary_resource = models.CharField(
        max_length=12, blank=True, null=True, choices=resource_choices
    )

    def reset_turn_based(self):
        self.primary_resource = None
        self.save()
        super(JoanPlayerMat, self).reset_turn_based()


class PlayerMatResourcePeople(models.Model):
    TYPE_CHOICES = (
        (VillagerType.GUARD.value, VillagerType.GUARD.name),
        (VillagerType.WORKER.value, VillagerType.WORKER.name),
    )

    player_mat = models.ForeignKey(PlayerMat, on_delete=models.CASCADE)
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    wood = models.BooleanField(default=False)
    stone = models.BooleanField(default=False)
    gold = models.BooleanField(default=False)
    land = models.BooleanField(default=False)
    iron = models.BooleanField(default=False)

    class Meta:
        unique_together = (("player_mat", "type"),)

    @property
    def type_name(self) -> str:
        return VillagerType(self.type).name

    @property
    def total(self) -> int:
        return sum([self.wood, self.stone, self.gold, self.land, self.iron])

    def has_resource(self, resource: ResourceType) -> bool:
        return self.__getattribute__(resource.name.lower())

    def _set_resource(self, resource: ResourceType, is_set: bool = True):
        self.__setattr__(resource.name.lower(), is_set)

    def remove_from_resource(self, resource: ResourceType):
        """
        Remove a villager from this resource.

        :param resource:
        :type resource: ResourceType
        :raises NoMoreOfVillagerError: All villagers have been removed
        :raises InvalidResourceForVillagerError: Resource has already been removed or is unset
        """

        if self.total == 0:
            raise NoMoreOfVillagerError(f"No more {self.type_name} villager to remove")

        if not self.has_resource(resource):
            raise InvalidResourceForVillagerError(
                f"Cannot remove {self.type_name} from {resource.name} when not set"
            )
        self._set_resource(resource, False)
        self.save()

    def add_to_resource(self, resource: Optional[ResourceType] = None):
        """
        Add a villager to this resource.

        :param resource: when missing, and this is a WORKER, goes in resource order
        :raises VillagerMaxedOutError: no more of this villager can be added
        :raises MissingGuardResourceError: guard requires a player to choose a resource
        :raises InvalidResourceForVillagerError: villager already set to this resource
        """
        if self.total == 5:
            raise VillagerMaxedOutError(f"Maxed out on {self.type_name} villager")

        if self.type == VillagerType.GUARD and resource is None:
            raise MissingGuardResourceError(f"Resource required for {self.type_name}")
        elif self.type == VillagerType.WORKER and resource is None:
            try:
                resource = self._get_next_worker_resource()
            except WorkersFullError:
                raise VillagerMaxedOutError("All worker resources are full")

        if self.has_resource(resource):
            raise InvalidResourceForVillagerError(
                f"Cannot add {self.type_name} to {resource.name} when already added"
            )

        self._set_resource(resource, True)
        self.save()

    def _get_next_worker_resource(self) -> ResourceType:
        for resource in list(ResourceType):
            if not self.has_resource(resource):
                return resource

        raise WorkersFullError("All worker resources are full")


class PlayerBuilt(models.Model):
    """
    The card that a player has built this game.
    """

    ANIMAL_CHOICES = [(name, name) for name in ANIMAL_PREFERENCE]
    ANIMAL_CHOICES.append(("", ""))

    player_mat = models.ForeignKey(PlayerMat, on_delete=models.CASCADE)
    card = models.CharField(max_length=52)
    count = models.PositiveSmallIntegerField(default=1)
    adds_animal = models.CharField(max_length=16, choices=ANIMAL_CHOICES)
