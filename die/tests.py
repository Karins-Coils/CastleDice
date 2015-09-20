"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import unittest
from die.dieClass import Die
from CD_globals import BARBARIAN, HORSE, PIG, COW, CHICKEN, \
    WOOD, STONE, GOLD, LAND, IRON

class TestDieClass(unittest.TestCase):

    def test_is_barbarian(self):
        self.assertTrue(Die.is_barbarian((BARBARIAN, 1)))
        self.assertTrue(Die.is_barbarian((u''+BARBARIAN, 1)))
        self.assertTrue(Die.is_barbarian([BARBARIAN, 1]))
        self.assertTrue(Die.is_barbarian([u''+BARBARIAN, 1]))
        self.assertFalse(Die.is_barbarian((LAND, 2)))
        self.assertFalse(Die.is_barbarian((u''+LAND, 2)))
        self.assertFalse(Die.is_barbarian([LAND, 2]))
        self.assertFalse(Die.is_barbarian([u''+LAND, 2]))
