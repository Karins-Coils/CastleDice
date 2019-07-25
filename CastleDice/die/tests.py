"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import unittest

from CastleDice.common.globals import BARBARIAN, LAND
from CastleDice.die.dieClass import Die


class TestDieClass(unittest.TestCase):
    def test_is_barbarian(self):
        self.assertTrue(Die.is_barbarian((BARBARIAN, 1)))
        self.assertTrue(Die.is_barbarian((u"" + BARBARIAN, 1)))
        self.assertTrue(Die.is_barbarian([BARBARIAN, 1]))
        self.assertTrue(Die.is_barbarian([u"" + BARBARIAN, 1]))
        self.assertFalse(Die.is_barbarian((LAND, 2)))
        self.assertFalse(Die.is_barbarian((u"" + LAND, 2)))
        self.assertFalse(Die.is_barbarian([LAND, 2]))
        self.assertFalse(Die.is_barbarian([u"" + LAND, 2]))
