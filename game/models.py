from django.conf import settings
from django.db import models
from jsonfield import JSONField


# Create your models here.

"""
game_id
turn_no - (1 to 7)
phase_no - (as shown on player mat)
player_order - stack?
world_pool - (choice) { Wood: 8, Gold: 9, ...}
             (gather) { Wood: [(Wood, 1), (Wood, 1), (Cow, 1)], Gold: []....}
"""


class Game(models.Model):
    turn_no = models.IntegerField()
    phase_no = models.IntegerField()
    player_order = JSONField()
    world_pool = JSONField()

    def __unicode__(self):
        return u'id '+str(self.id)


"""
user_id
game_id
hand - { Castle: [ ....], Villager: [ ....], Market: [....]}
animals - {Horse: 0, Chicken: 0, Pig: 1, Cow: 1}
villagers - {Worker: 1, Guard: [Iron], Merchant: 1, Farmer: 0}
built -
resources - {Wood: 1, Stone: 2, Gold: 0, Land: 3, Iron: 0}
dice_chosen - [Wood, Wood, Stone, Land, Iron, Gold, Gold]
dice_rolled - {Wood: (Barbarian, 1)}
"""


class PlayerMat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    game = models.ForeignKey('Game')
    resources = JSONField()
    animals = JSONField()
    villagers = JSONField()
    built = JSONField()
    dice_chosen = JSONField()
    dice_rolled = JSONField()

    def __unicode__(self):
        return u'id '+str(self.id)
