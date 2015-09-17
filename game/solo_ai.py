__author__ = 'kelseyhawley'

from CD_globals \
    import Horse, Pig, Cow, Chicken, Barn, Wood, Stone, Gold, Land, Iron, \
    ResourcePreference, AnimalPreference

"""
Idea, is a class that handles all the logic, and then returns the only things
that are required for an update to the db, etc


"""


class Joan:
    # current count of Joan's animals
    animals = {
        Horse: 0,
        Cow: 0,
        Pig: 0,
        Chicken: 0
    }
    # primary resource that Joan is focused on gathering
    resource = None

    def __init__(self, animals=None, resource=None):
        if animals:
            self.animals = animals

        if resource:
            self.resource = resource

    @staticmethod
    def determine_primary_resource(dice_list):
        """Take in a given choice dice list, and determine Joan's primary

        Args:
        dice_list -- list of dice, only uses the die type

        Returns & Sets
        self.resource -- the string & die type/primary resource

        """

        max_count = 0
        max_resource = []
        unique_dice = set(dice_list)

        # loop through list find highest count.  create a list if a tie
        for die in unique_dice:
            count = dice_list.count(die)
            if max_count < count:
                max_count = count
                max_resource = [die]
            elif max_count == count:
                max_resource.append(die)

        if len(max_resource) is 1:
            # we are done, Joan has a CLEAR primary resource
            return max_resource[0]
        else:
            # its a list because of a tie, need to pick best option
            count = 5
            for resource in max_resource:
                i = ResourcePreference.index(resource)
                if i < count:
                    prime_resource = resource
                    count = i

            return prime_resource
