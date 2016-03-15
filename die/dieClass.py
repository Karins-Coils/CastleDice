import random

from common.dice import DICE_FACES, BARBARIAN


class Die:
    resource = ""
    ## resource tracks what kind of die is being rolled: Wood, Stone, Gold, etc
    sides = []
    debug = False

    def __init__(self, resource=None, debug=False):
        self.resource = resource
        self.debug = debug
        self.create_die()

    def __str__(self):
        sides = ""
        for i in range(len(self.sides)):
            sides += str(self.sides[i])
            if i < len(self.sides) - 1:
                sides += ", "
        return self.resource + ": [ " + sides + " ]"

    def create_die(self):
        if self.resource:
            self.sides = DICE_FACES[self.resource]
            self.resource = self.resource.capitalize()
        else:
            self.sides = [1, 2, 3, 4, 5, 6]
            self.resource = "6-sided"

    def roll_die(self):
        roll = random.randint(0, 5)
        if self.debug:
            print "rolled " + str(roll) + "\n"
        resource, count = self.sides[roll]
        return resource, count

    @staticmethod
    def roll_multiple_die(die_set):
        for d in die_set:
            print d.resource + ": " + str(d.roll_die())

    @staticmethod
    def roll_and_total_dice(die_set):
        r_rolled = {}
        for d in die_set:
            r, count = d.roll_die()
            print d.resource + " die: " + str(count) + " " + r
            if r in r_rolled:
                r_rolled[r] += count
            else:
                r_rolled[r] = count
        print r_rolled

    @staticmethod
    def total_dice(rolled_die):
        # takes in list formatted like so:
        # ( (dice_type, (resource, count)), ...)
        r_rolled = {}
        for d, roll in rolled_die:
            resource, count = roll
            if resource in r_rolled:
                r_rolled[resource] += count
            else:
                r_rolled[resource] = count
        return r_rolled

    @staticmethod
    def is_barbarian(die_face):
        return die_face[0] == BARBARIAN
