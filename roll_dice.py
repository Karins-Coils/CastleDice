#!/usr/bin/env python2.7
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


class Die:
	resource = ""  ## this tracks what kind of die is being rolled: Wood, Stone, Gold, etc
	sides = []
	debug = False

	def __init__(self, resource, debug = False):
		self.resource = resource
		self.debug = debug
		self.create_die()

	def __str__(self):
		sides = ""
		for i in range(len(self.sides)):
			sides += str(self.sides[i])
			if i < len(self.sides)-1:
				sides += ", "
		return self.resource +": [ "+ sides+" ]"


	def create_die(self):
		if self.resource ==  Wood:
			self.sides = [(Wood, 1), (Wood, 1), (Wood, 2), (Wood, 3), (Cow, 1), (Barbarian, 1)]
		elif self.resource == Stone:
			self.sides = [(Stone, 1), (Stone, 1), (Stone, 2), (Stone, 2), (Chicken, 1), (Barbarian, 1)]
		elif self.resource == Gold:
			self.sides = [(Gold, 1), (Gold, 1), (Gold, 1), (Gold, 2), (Horse, 1), (Barbarian, 1)]
		elif self.resource == Land:
			self.sides = [(Land, 1), (Land, 1), (Land, 2), (Pig, 1), (Pig, 1), (Barbarian, 1)]
		elif self.resource == Iron:
			self.sides = [(Iron, 1), (Iron, 2), (Pig, 1), (Horse, 1), (Chicken, 1), (Barbarian, 1)]
		else:
			self.sides = [1,2,3,4,5,6]

		self.resource = self.resource.capitalize()

	def roll_die(self):
		roll = random.randint(0,5)
		if self.debug: print "rolled " + str(roll) + "\n"
		resource, count = self.sides[roll]
		return resource, count

def roll_multiple_die(dieSet):
	for d in dieSet:
		print d.resource +": "+ str(d.roll_die())

def roll_and_total_dice(dieSet):
	r_rolled = {}
	for d in dieSet:
		r, count = d.roll_die()
		print d.resource +" die: "+ str(count) +" "+ r
		if r_rolled.has_key(r):
			r_rolled[r] += count
		else:
			r_rolled[r] = count
	print r_rolled


dieSet = [
	Die(Wood),
	Die(Stone),
	Die(Gold),
	Die(Land),
	Die(Iron),
	Die(Wood),
	Die(Stone),
	Die(Wood)

]
roll_multiple_die(dieSet)
print
print
roll_and_total_dice(dieSet)
