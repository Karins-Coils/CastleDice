# from django.contrib.auth.models import User

from common.globals import BARN, JOAN, TURN, \
    RESOURCE_PREFERENCE, ANIMAL_PREFERENCE, GATHER_PREFERENCE
from die.dieClass import Die

"""
Joan is a simplistic AI built for solo play.  She uses a dice to determine
which die to roll into the world pool.  And gathers with a very specific logic:
- First her highest value priority die
- If none, rolls:
- - If resource, gather highest of that
- - If barn, choose her most valued animal
- - Else pick the rarest & highest resource

"""


class JoanAI(object):

    def __init__(self, **kwargs):
        self.animals = kwargs["animals"] if "animals" in kwargs else None
        self.resource = kwargs["resource"] if "resource" in kwargs else None

    @staticmethod
    def choose_dice(turn_no, pool_count_dict):
        """choose her dice for this turn from the remaining in the world

        Roll her dice to create a list of len TURN[turn_no]['no_choices'].
        If Barn, some repetition is created toward the former or previous roll.
        If rolling barns TOO many times, and list is unruly, splice before
        returning it.

        Args:
            turn_no: int, to be used in TURN
            pool_count_dict: dict of current count of dice in the pool
                ex: global DICE_COUNT - {WOOD: 3, STONE: 5, ....}

        Returns:
            list of die choices
                ex: [WOOD, WOOD, IRON]

        """
        choice_dice = []
        #roll Joan die to determine her choice

        append_count = 1
        while True:
            die = Die(JOAN).roll_die()[0]
            if die is not BARN:
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
            if len(choice_dice) >= TURN[turn_no]['no_choices']:
                break

        # return list splice, just in case I rolled a bunch of barns in a row
        return choice_dice[0:TURN[turn_no]['no_choices']]

    @staticmethod
    def gather_die(primary_resource, world_pool_dict, die_choice=None):
        """Based on her logic, picks a die from the passed in world_pool_dict

        Flattens the world_pool_dict into a set, then orders it based on her
        preferences.  Looks for her primary resource (self.resource) first,
        then rolls to determine what she will look for next (resource or
        animal).  If none, then grabs the rarest & highest value resource left.

        Args:
            primary_resource: str, no longer stored on class, passed in order
                to be static
                ex: WOOD
            world_pool_dict: a dict of lists of tuples
                ex: { WOOD: [(WOOD, 1), (COW, 1)], STONE: [(CHICKEN, 1)], ... }
            die_choice: str
                optional, mostly used to test without randomness of rolling

        Returns:
            tuple of die side value
                ex: (CHICKEN, 1)

        """

        resource = primary_resource if not die_choice else die_choice

        # flatten dict values, then make set
        world_pool_set = sorted(
            [tup for val_list in world_pool_dict.values()
             for tup in set(val_list)],
            key=lambda t: (GATHER_PREFERENCE.index(t[0]), -t[1])
        )

        while True:
            # first chooses of her resource, if available
            if resource is not BARN and world_pool_dict[resource]:

                primary_choices = [x for x in world_pool_set
                                   if x[0] is resource]
                if primary_choices:
                    return primary_choices[0]

            # rolled a barn
            elif resource is BARN:
                # gather highest animal
                primary_choices = [x for x in world_pool_set
                                   if x[0] in ANIMAL_PREFERENCE]
                if primary_choices:
                    return primary_choices[0]

            # if still none & have not rolled yet, then rolls the die
            if not die_choice:
                die_choice = Die(JOAN).roll_die()[0]
            else:
                # rolled it once already, return the rarest+highest resource
                primary_choices = [x for x in world_pool_set
                                   if x[0] in RESOURCE_PREFERENCE]
                if primary_choices:
                    return primary_choices[0]

    @staticmethod
    def determine_primary_resource(dice_list):
        """Take in a given choice dice list, and return Joan's primary resource

        Creates a list tuples, (type, count) based on dice_list, then finds the
        max such that the count is used as a determinant first, then if a tie,
        looks at RESOURCE_PREFERENCE to weigh the type correctly.  (negated
        below to account for max wanting a LARGE integer, rather than the small
        index)

        Args:
            dice_list: list of dice, only uses the die type
                ex: [WOOD, WOOD, IRON, LAND]

        Returns:
            the string & die type/primary resource
                ex: WOOD

        """

        return max(
            # this creates a generator for one tuple, rather than a full list
            # memory saving.  Thanks erich!
            ((x, dice_list.count(x)) for x in set(dice_list)),
            key=lambda t: (t[1], -RESOURCE_PREFERENCE.index(t[0]))
        )[0]
