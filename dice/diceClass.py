import random
import CD_globals as CD

# Resources
## Building Materials
Wood = CD.Wood
Stone = CD.Stone
Gold = CD.Gold
Land = CD.Land
Iron = CD.Iron
## Animals
Horse = CD.Horse
Pig = CD.Pig
Cow = CD.Cow
Chicken = CD.Chicken
## Lone Barbarian
Barbarian = CD.Barbarian


class Die:
    resource = ""
    ## resource tracks what kind of die is being rolled: Wood, Stone, Gold, etc
    sides = []
    debug = False

    def __init__(self, resource, debug=False):
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
            self.sides = CD.DiceFaces[self.resource]
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


def roll_multiple_die(die_set):
    for d in die_set:
        print d.resource + ": " + str(d.roll_die())


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
