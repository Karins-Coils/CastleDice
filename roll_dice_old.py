import random

# Resources
## Building Materials
Wood ='wood'
Stone = 'stone'
Gold = 'gold'
Land = 'land'
Iron = 'iron'
## Animals
Horse = 'horse'
Pig = 'pig'
Cow = 'cow'
Chicken = 'chicken'
## Lone Barbarian
Barbarian = 'barbarian'


class Dice:
	chosenResource = ""  ## this tracks what kind of die is being rolled: Wood, Stone, Gold, etc
	chosenDie = []
	debug = False

	def __init__(self, resource, debug = False):
		self.chosenResource = resource
		self.debug = debug
		self.create_die()

	def __str__(self):
		sides = ""
		for i in range(len(self.chosenDie)):
			sides += str(self.chosenDie[i])
			if i < len(self.chosenDie)-1:
				sides += ", "
		return self.chosenResource +": [ "+ sides+" ]"


	def create_die(self):
		if self.chosenResource ==  Wood:
			self.chosenDie = [DieSide(Wood), DieSide(Wood), DieSide(Wood, 2), DieSide(Wood, 3), DieSide(Cow), DieSide(Barbarian)]
		elif self.chosenResource == Stone:
			self.chosenDie = [DieSide(Stone), DieSide(Stone), DieSide(Stone, 2), DieSide(Stone, 2), DieSide(Chicken), DieSide(Barbarian)]
		elif self.chosenResource == Gold:
			self.chosenDie = [DieSide(Gold), DieSide(Gold), DieSide(Gold), DieSide(Gold, 2), DieSide(Horse), DieSide(Barbarian)]
		elif self.chosenResource == Land:
			self.chosenDie = [DieSide(Land), DieSide(Land), DieSide(Land, 2), DieSide(Pig), DieSide(Barbarian)]
		elif self.chosenResource == Iron:
			self.chosenDie = [DieSide(Iron), DieSide(Iron, 2), DieSide(Pig), DieSide(Horse), DieSide(Chicken), DieSide(Barbarian)]
		else:
			self.chosenDie = [1,2,3,4,5,6]

	def roll_dice(self):
		roll = random.randint(0,5)
		if self.debug: print "rolled " + str(roll) + "\n"
		chosenRoll = self.chosenDie[roll]
		return chosenRoll


class DieSide:
	side = ""
	count = 0

	def __init__(self, resource, count = 1):
		self.side = resource
		self.count = count

	def __str__(self):
		return self.side+" "+str(self.count)

	def __int__(self):
		return self.count

def roll_multiple_dice(dieSet):
	for d in dieSet:
		print d.chosenResource +": "+ str(d.roll_dice())

#def roll_and_total_dice()

dieSet = [
	Dice(Wood),
	Dice(Stone),
	Dice(Gold),
	Dice(Land),
	Dice(Iron)
]
roll_multiple_dice(dieSet)
