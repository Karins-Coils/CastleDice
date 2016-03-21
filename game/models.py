from collections import defaultdict

from annoying.fields import JSONField
from django.contrib.auth.models import User
from django.db import models

from common.dice import DICE_COUNT
from common.cards import GAME_DECK_NAMES
from common.globals import TURN


class Game(models.Model):
    is_solo_game = models.BooleanField(default=False)
    current_player = models.ForeignKey(User,
                                       related_name='+',
                                       blank=True,
                                       null=True)
    current_turn = models.PositiveSmallIntegerField(default=1)
    current_phase = models.PositiveSmallIntegerField(default=1)
    choice_dice = JSONField(blank=True, null=True, default=[])
    gather_dice = JSONField(blank=True, null=True, default={})
    true_porkchop_used = models.BooleanField(default=False)

    def setup_choice_dice_for_turn(self):
        player_count = self.playermat_set.count()
        given_dice = TURN[self.current_turn]['given_dice']

        # setup base choice die for all players
        for playermat in self.playermat_set.all():
            playermat.choice_dice = given_dice
            playermat.save()

        # create choice pool from remaining dice
        # get count for this resource, multiply by players
        # subtract the already claimed dice from the remaining pool
        total_dice = {
            resource: value - (given_dice.get(resource, 0) * player_count)
            for resource, value in DICE_COUNT.iteritems()
        }
        self.choice_dice = total_dice
        self.save()

    def advance_turn(self):
        # custom logic to advance turn & reset base values
        # confirm barbarians phase completed
        self.game.current_turn += 1
        self.game.current_phase = 1
        self.game.current_player = None
        self.game.choice_dice = None
        self.game.gather_dice = None  # should already be cleared
        self.true_porkchop_used = False

        self.save()

    def advance_phase(self):
        # custom logic to check if all players have had their turn
        # or other conditions met (gathered all dice, etc)
        self.current_phase += 1
        self.current_player = self.playermat_set.get(player_order=1)

        self.save()

    def advance_current_player(self):
        """
        Based on game.current_player & each playermat.player_order,
        set game.current_player to the next player in order
        Used during a turn, after player_order has already been set.
        :return:
        """
        # get the current player's order
        current_player_order = self.playermat_set.get(
            player=self.current_player)

        # if the player_order is equal to the total number of players,
        # go back to the first player
        if current_player_order == self.playermat_set.count():
            self.current_player = self.playermat_set.get(player_order=1)

        # else get the player with the next highest player_order
        else:
            self.current_player = self.playermat_set.get(
                player_order=current_player_order+1)

        self.save()

    def determine_player_order(self):
        # first turn, no player order set yet, no horses
        if self.turn == 1:
            initial_order = 1
            for playermat in self.playermat_set.all().order_by('id'):
                # initial turn, just go clockwise
                playermat.player_order = initial_order
                playermat.save()
                initial_order += 1
            return

        # check for clear max_horses
        max_horses = self.playermat_set.all().order_by('-horses')[0]
        if max_horses > 0 and \
                self.playermat_set.filter(horses=max_horses).count() == 1:
            player_one = self.playermat_set.get(horses=max_horses)
            player_one_idx = None
            for idx, playermat in enumerate(self.playermat_set.order_by('id')):
                if playermat.id == player_one.id:
                    player_one_idx = idx
                    break

            initial_order = 1
            for idx in [range(player_one_idx, self.playermat_set.all().count())] + [range(0, player_one_idx)]:
                playermat = self.playermat_set.order_by('id')[idx]
                playermat.player_order = initial_order
                playermat.save()
                initial_order += 1
            return

        # no max horses, simply increment the player_order
        for playermat in self.playermat_set.all().order_by('player_order'):
            if playermat.player_order == self.playermat_set.count():
                playermat.player_order = 1
            else:
                playermat.player_order += 1
            playermat.save()

    def get_current_player_playermat(self):
        return self.playermat_set.get(id=self.current_player)

    def add_dice_to_world(self, die_dict):
        if not self.gather_dice:
            self.gather_dice = {}
        for resource_type, die_faces_list in die_dict.items():
            self.gather_dice[resource_type] = self.gather_dice.get(resource_type, []) + die_faces_list
        self.save()
