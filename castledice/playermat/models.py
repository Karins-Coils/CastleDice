from typing import Optional

from annoying.fields import JSONField
from django.conf import settings
from django.db import models, transaction

from castledice.common.constants import GameConstants, ResourceType, VillagerType
from castledice.common.globals import ANIMAL_PREFERENCE, BARBARIAN, RESOURCE_PREFERENCE
from castledice.die.dieClass import Die
from castledice.game.turns import Turn

from .exceptions import (
    InvalidResourceForVillagerError,
    MissingGuardResourceError,
    NoMoreOfVillagerError,
    UnknownVillagerTypeError,
    VillagerMaxedOutError,
    VillagerTypeCannotHaveResourcesError,
    VillagerTypeMustHaveResourcesError,
    WorkersFullError,
)

_VILLAGERS_ASSIGNED_RESOURCES = (VillagerType.GUARD, VillagerType.WORKER)
_VILLAGERS_NOT_ASSIGNED_RESOURCES_MAX = 3
_VILLAGERS_ASSIGNED_RESOURCES_MAX = 5


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

    @property
    def workers_mat(self) -> "PlayerMatResourcePeople":
        return self.get_mat_for_villager(VillagerType.WORKER)

    @property
    def guards_mat(self) -> "PlayerMatResourcePeople":
        return self.get_mat_for_villager(VillagerType.GUARD)

    def get_mat_for_villager(self, villager: VillagerType):
        if villager not in _VILLAGERS_ASSIGNED_RESOURCES:
            raise VillagerTypeMustHaveResourcesError(
                f"This method does not work for {villager.name}"
            )

        villager_mat, _ = self.playermatresourcepeople_set.get_or_create(type=villager)
        return villager_mat

    def get_villager_count(self, villager: VillagerType):
        if villager in _VILLAGERS_ASSIGNED_RESOURCES:
            raise VillagerTypeCannotHaveResourcesError(
                f"Villager type {villager.name} is assigned a resource and cannot use this method"
            )
        attr_name = f"{villager.name.lower()}s"
        return getattr(self, attr_name)

    def _set_villager_count(self, villager: VillagerType, count: int):
        attr_name = f"{villager.name.lower()}s"
        setattr(self, attr_name, count)

    def get_resource_count(self, resource: ResourceType) -> int:
        attr_name = resource.name.lower()
        return getattr(self, attr_name)

    def _set_resource_count(self, resource: ResourceType, amount: int):
        attr_name = resource.name.lower()
        setattr(self, attr_name, amount)

    def get_player_choice_extra_dice(self):
        # based on turn no, get number of 'extra' dice player will choose
        # TODO: logic to confirm if player has Royal Chambers etc
        return Turn(self.game.current_turn.turn_no).number_of_choices

    def add_resource(self, resource: ResourceType, add_amount: int = 1):
        """
        Match the resource to the column and add amount to value
        """
        current_amount = self.get_resource_count(resource)
        # adding more than the allowed max
        new_amount = min(current_amount + add_amount, GameConstants.MAX_RESOURCES)

        self._set_resource_count(resource, new_amount)
        self.save()

    def remove_resource(self, resource: ResourceType, remove_amount: int = 1):
        """
        Match resource to column and remove count, default 1
        """
        current_amount = self.get_resource_count(resource)
        # cannot have a negative amount of a resource
        new_amount = max(current_amount - remove_amount, 0)

        self._set_resource_count(resource, new_amount)
        self.save()

    def add_villager(
        self,
        villager: VillagerType,
        add_amount: int = 1,
        to_resource: Optional[ResourceType] = None,
    ):
        """
        Add the given villager type to the playermat.
        """

        # check that the resource type is allowed
        # check that the is space to add another of x type

        if villager == VillagerType.BARBARIAN:
            self.add_barbarian(add_amount)

        elif villager == VillagerType.WORKER:
            self.add_worker(add_amount, to_resource)

        elif villager == VillagerType.GUARD:
            if add_amount > 1:
                raise MissingGuardResourceError(
                    "Tried to add multiple guards with only one resource"
                )
            self.add_guard(to_resource)

        elif villager == VillagerType.MERCHANT:
            self.add_merchant(add_amount)

        elif villager == VillagerType.FARMER:
            self.add_farmer(add_amount)

        else:
            raise UnknownVillagerTypeError(
                f"Villager type {villager.name} not found when adding to mat"
            )

    def add_barbarian(self, amount: int = 1):
        # barbarians have no max
        self.barbarians += amount
        self.save()

    def _add_merchant_or_farmer(self, villager: VillagerType, add_amount: int):
        current_amount = self.get_villager_count(villager)

        if current_amount + add_amount > 3:
            raise VillagerMaxedOutError(f"Can't have more than 3 {villager.name}")

        self._set_villager_count(villager, current_amount + add_amount)
        self.save()

    def add_merchant(self, amount: int = 1):
        """Simple wrapper to add a merchant"""
        self._add_merchant_or_farmer(VillagerType.MERCHANT, amount)

    def add_farmer(self, amount: int = 1):
        """Simple wrapper to add a farmer"""
        self._add_merchant_or_farmer(VillagerType.FARMER, amount)

    def add_worker(self, amount: int = 1, resource: ResourceType = None):
        """More complex wrapper around workers_mat call"""
        if self.workers_mat.total + amount > 5:
            raise VillagerMaxedOutError("Can't have more than 5 workers")

        if amount == 1 and resource is not None:
            self.workers_mat.add_to_resource(resource)
            return

        if resource is not None:
            raise InvalidResourceForVillagerError(
                "Too many workers for a specific Resource"
            )

        for _ in range(amount):
            self.workers_mat.add_to_resource()

    def add_guard(self, resource: ResourceType):
        """Simple wrapper around the guard_mat call"""
        self.guards_mat.add_to_resource(resource)

    def remove_villager(
        self,
        villager: VillagerType,
        remove_amount: int = 1,
        from_resource: Optional[ResourceType] = None,
    ):
        if villager == VillagerType.BARBARIAN:
            self.remove_barbarian(remove_amount)

        elif villager == VillagerType.WORKER:
            if remove_amount > 1 or from_resource is None:
                raise InvalidResourceForVillagerError(
                    "Only worker from a specific resource can be removed"
                )
            self.remove_worker(from_resource)

        elif villager == VillagerType.GUARD:
            if remove_amount > 1 or from_resource is None:
                raise InvalidResourceForVillagerError(
                    "Only guard from a specific resource can be removed"
                )
            self.remove_guard(from_resource)

        elif villager == VillagerType.MERCHANT:
            self.remove_merchant(remove_amount)

        elif villager == VillagerType.FARMER:
            self.remove_farmer(remove_amount)

        else:
            raise UnknownVillagerTypeError(
                f"Villager type {villager.name} not found when adding to mat"
            )

    def remove_barbarian(self, remove_amount: int = 1):
        # ensure that the lowest value is 0
        self.barbarians = max(self.barbarians - remove_amount, 0)

    def _remove_merchant_or_farmer(self, villager: VillagerType, remove_amount: int):
        attr_name = f"{villager.name.lower()}s"
        current_amount = getattr(self, attr_name)

        if current_amount - remove_amount < 0:
            raise NoMoreOfVillagerError(
                f"Tried to remove more {attr_name} than available: remove {remove_amount} from {current_amount}"
            )

        setattr(self, attr_name, current_amount - remove_amount)
        self.save()

    def remove_worker(self, resource: ResourceType):
        """Simple wrapper"""
        self.workers_mat.remove_from_resource(resource)

    def remove_guard(self, resource: ResourceType):
        """Simple wrapper"""
        self.guards_mat.remove_from_resource(resource)

    def remove_farmer(self, amount: int = 1):
        self._remove_merchant_or_farmer(VillagerType.FARMER, amount)

    def remove_merchant(self, amount: int = 1):
        self._remove_merchant_or_farmer(VillagerType.MERCHANT, amount)

    def convert_villager(
        self,
        current_villager: VillagerType,
        new_villager: VillagerType,
        current_resource: ResourceType = None,
        new_resource: ResourceType = None,
    ):
        """
        :param current_villager: the existing villager that will be converted
        :param new_villager: the new villager we want to have
        :param current_resource: the resource (if applicable) of the current villager
        :param new_resource: the resource (if applicable_ of the new villager
        """

        # confirm current villager exists
        if current_villager in _VILLAGERS_ASSIGNED_RESOURCES:
            # confirm resource passed if required
            if current_resource is None:
                raise InvalidResourceForVillagerError(
                    f"The current villager type {current_villager.name} requires a resource to be selected"
                )

            villager_mat = self.get_mat_for_villager(current_villager)
            if not villager_mat.has_resource(current_resource):
                raise NoMoreOfVillagerError(
                    f"No more {current_villager.name} villagers of type {current_resource.name}"
                )
        else:
            current_villager_count = self.get_villager_count(current_villager)
            if current_villager_count < 1:
                raise NoMoreOfVillagerError(
                    f"No more {current_villager.name} left to convert"
                )

        # confirm space for new_villager type
        if new_villager in _VILLAGERS_ASSIGNED_RESOURCES:
            # confirm resource if required
            if new_villager in _VILLAGERS_ASSIGNED_RESOURCES and new_resource is None:
                raise InvalidResourceForVillagerError(
                    f"The new villager type {new_villager.name} requires a resource to be selected"
                )
            # and space on the specified resource
            villager_mat = self.get_mat_for_villager(new_villager)
            if villager_mat.has_resource(new_resource):
                raise InvalidResourceForVillagerError(
                    f"Can only have one {new_villager.name} villagers of type {new_resource.name}"
                )
        else:
            new_villager_count = self.get_villager_count(new_villager)
            if new_villager_count == _VILLAGERS_NOT_ASSIGNED_RESOURCES_MAX:
                raise VillagerMaxedOutError(f"No more {new_villager.name} allowed")

        # preconditions have passed - remove existing + add new in same transaction
        with transaction.atomic():
            self.remove_villager(current_villager, from_resource=current_resource)
            self.add_villager(new_villager, to_resource=new_resource)

    def reset_turn_based(self):
        self.has_porkchopped = False
        self.has_first_gathered = False
        self.has_farmered = False
        self.choice_dice = False
        self.barbarians = 0
        self.save()

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
        return getattr(self, resource.name.lower())

    def _set_resource(self, resource: ResourceType, is_set: bool = True):
        setattr(self, resource.name.lower(), is_set)

    def remove_from_resource(self, resource: ResourceType):
        """
        Remove a villager from this resource.

        :param resource:
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
