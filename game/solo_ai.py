from CD_globals \
    import Horse, Pig, Cow, Chicken, Barn, \
    Wood, Stone, Gold, Land, Iron, Joan, \
    ResourcePreference, AnimalPreference, GatherPreference, Turn
from dice.diceClass import Die

"""
Idea, is a class that handles all the logic, and then returns the only things
that are required for an update to the db, etc


"""


class JoanAI:
    # current count of Joan's animals
    animals = {
        Horse: 0,
        Cow: 0,
        Pig: 0,
        Chicken: 0
    }
    # primary resource that Joan is focused on gathering
    resource = None

    def __init__(self, **kwargs):
        self.animals = kwargs["animals"] if "animals" in kwargs else None
        self.resource = kwargs["resource"] if "resource" in kwargs else None

    @staticmethod
    def choose_dice(turn_no, pool_count_dict):
        """choose her dice for this turn from the remaining in the world"""
        choice_dice = []
        #roll Joan die to determine her choice

        append_count = 1
        while True:
            die = Die(Joan).roll_die()[0]
            if die is not Barn:
                # append the non-Barn
                choice_dice += [die for i in xrange(0, append_count)]
                # decrement the pool count, to keep track locally
                pool_count_dict[die] -= append_count
                append_count = 1
            elif choice_dice:
                # append a repeat of last die
                choice_dice.append(choice_dice[-1])
            else:
                # append the NEXT die twice...
                append_count += 1
            if len(choice_dice) >= Turn[turn_no]['no_choices']:
                break

        # return list splice, just in case I rolled a bunch of barns in a row
        return choice_dice[0:Turn[turn_no]['no_choices']]


    def gather_die(self, world_pool_dict, die_choice=None):
        """
        assume world_pool_dict: { "wood": [(wood, 1), (cow, 1)] .....}

        """
        if not self.resource:
            raise ValueError("Joan.resource has not been set")

        if not self.resource in world_pool_dict:
            raise ValueError("Joan.resource not found in world_pool_dict, "
                             "may have been improperly set")

        resource = self.resource if not die_choice else die_choice

        # flatten dict values, then make set
        world_pool_set = sorted(
            [tup for val_list in world_pool_dict.values()
             for tup in set(val_list)],
            key=lambda t: (GatherPreference.index(t[0]), -t[1])
        )

        while True:
            # first chooses of her resource
            if resource is not Barn and world_pool_dict[resource]:

                primary_choices = [x for x in world_pool_set if x[0] is resource]
                if primary_choices:
                    return primary_choices[0]

            # rolled a barn
            elif resource is Barn:
                # gather highest animal
                primary_choices = [x for x in world_pool_set
                                   if x[0] in AnimalPreference]
                if primary_choices:
                    return primary_choices[0]

            # if still none & have not rolled yet, then rolls the die
            if not die_choice:
                die_choice = Die(Joan).roll_die()[0]
            else:
                # rolled it once already, so just return the rarest+highest
                primary_choices = [x for x in world_pool_set
                                   if x[0] in ResourcePreference]
                if primary_choices:
                    return primary_choices[0]

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
