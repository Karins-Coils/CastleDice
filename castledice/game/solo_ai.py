from castledice.common.globals import (
    ANIMAL_PREFERENCE,
    BARN,
    GATHER_PREFERENCE,
    JOAN,
    RESOURCE_PREFERENCE,
    TURN,
)
from castledice.die.dieClass import Die
from castledice.playermat.models import JoanPlayerMat
from castledice.users.models import User

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
        # roll Joan die to determine her choice

        append_count = 1
        while True:
            die = Die(JOAN).roll_die()[0]
            if die is not BARN:
                # append the non-Barn
                choice_dice += [die for i in range(0, append_count)]
                # decrement the pool count, to keep track locally
                pool_count_dict[die] -= append_count
                append_count = 1
            elif choice_dice:
                # append a repeat of last die
                choice_dice.append(choice_dice[-1])
            else:
                # append the NEXT die twice...
                append_count += 1
            if len(choice_dice) >= TURN[turn_no]["no_choices"]:
                break

        # return list splice, just in case I rolled a bunch of barns in a row
        return choice_dice[0 : TURN[turn_no]["no_choices"]]

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
            [tup for val_list in world_pool_dict.values() for tup in set(val_list)],
            key=lambda t: (GATHER_PREFERENCE.index(t[0]), -t[1]),
        )

        while True:
            # first chooses of her resource, if available
            if resource is not BARN and world_pool_dict[resource]:

                primary_choices = [x for x in world_pool_set if x[0] is resource]
                if primary_choices:
                    return primary_choices[0]

            # rolled a barn
            elif resource is BARN:
                # gather highest animal
                primary_choices = [
                    x for x in world_pool_set if x[0] in ANIMAL_PREFERENCE
                ]
                if primary_choices:
                    return primary_choices[0]

            # if still none & have not rolled yet, then rolls the die
            if not die_choice:
                die_choice = Die(JOAN).roll_die()[0]
            else:
                # rolled it once already, return the rarest+highest resource
                primary_choices = [
                    x for x in world_pool_set if x[0] in RESOURCE_PREFERENCE
                ]
                if primary_choices:
                    return primary_choices[0]

    @staticmethod
    def determine_primary_resource(dice_dict):
        """Take in a given choice dice list, and return Joan's primary resource

        Creates a list tuples, (type, count) based on dice_list, then finds the
        max such that the count is used as a determinant first, then if a tie,
        looks at RESOURCE_PREFERENCE to weigh the type correctly.  (negated
        below to account for max wanting a LARGE integer, rather than the small
        index)

        Args:
            dice_dict: dict of dice counts, only uses the die type
                ex: {WOOD: 3, IRON: 1, LAND: 2}

        Returns:
            the string & die type/primary resource
                ex: WOOD

        """

        return max(
            # this creates a generator for one tuple, rather than a full list
            # memory saving.  Thanks erich!
            dice_dict.items(),
            key=lambda t: (t[1], -RESOURCE_PREFERENCE.index(t[0])),
        )[0]

    @staticmethod
    def get_user_joan():
        """
        Will get or create user Joan
        :return: Joan user object
        :rtype: User
        """
        # return is a tuple: Tuple[User, bool], where bool is whether the obj was created
        u, _ = User.objects.get_or_create(
            username="JOAN_AI", email="joan@karinscoils.com"
        )
        return u


class JoanActions(object):
    @classmethod
    def execute(cls, game_obj):
        """

        :param game.models.Game game_obj:
        :return:
        """
        joan_playermat = JoanPlayerMat.objects.get_or_create(game=game_obj)[0]

        if game_obj.current_phase == 3:
            cls.phase_three(game_obj, joan_playermat)
        elif game_obj.current_phase == 5:
            cls.phase_five(game_obj, joan_playermat)
        elif game_obj.current_phase == 6:
            cls.phase_six(game_obj, joan_playermat)

    # choose dice
    @staticmethod
    def phase_three(game_obj, joan_playermat):
        new_choices = JoanAI.choose_dice(game_obj.current_turn, game_obj.choice_dice)

        for choice in new_choices:
            joan_playermat.choice_dice[choice] = (
                joan_playermat.choice_dice.get(choice, 0) + 1
            )

        joan_playermat.primary_resource = JoanAI.determine_primary_resource(
            joan_playermat.choice_dice
        )
        joan_playermat.save()

    # gather dice
    @staticmethod
    def phase_five(game_obj, joan_playermat):
        resource_tuple = JoanAI.gather_die(
            joan_playermat.primary_resource, game_obj.gather_dice
        )
        joan_playermat.add_resource(resource_tuple)

    # go to market
    @staticmethod
    def phase_six(game_obj, joan_playermat):
        if game_obj.current_turn in [3, 5, 7]:
            joan_playermat.go_to_market(max=True)
