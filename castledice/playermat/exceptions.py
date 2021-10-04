class VillagerMaxedOutError(Exception):
    """No more space for this type of Villager"""


class WorkersFullError(VillagerMaxedOutError):
    """Thrown when trying to add a new worker to an already full playmat"""


class MissingGuardResourceError(Exception):
    """Guards require a resource to be assigned"""


class InvalidResourceForVillagerError(Exception):
    """Villager already added or removed this resource"""


class NoMoreOfVillagerError(Exception):
    """No more remaining villagers of that type"""


class UnknownVillagerType(Exception):
    """No match for villager type"""
