import random

from annoying.fields import JSONField
from django.contrib.auth.models import User
from django.db import models

from .solo_ai import JoanAI

from ..common.dice import DICE_COUNT
from ..common.globals import TURN


class Game(models.Model):
    is_solo_game = models.BooleanField(default=False)
    current_player = models.ForeignKey(User,
                                       on_delete=models.CASCADE,
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
            for resource, value in DICE_COUNT.items()
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
        self.current_player = self.playermat_set.get(player_order=1).player

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
            player=self.current_player).player_order

        # if the player_order is equal to the total number of players,
        # go back to the first player
        if current_player_order == self.playermat_set.count():
            self.current_player = self.playermat_set.get(player_order=1).player

        # else get the player with the next highest player_order
        else:
            self.current_player = self.playermat_set.get(
                player_order=current_player_order + 1).player

        self.save()

    def determine_player_order(self):
        playermats = self.playermat_set.all().order_by('id')
        playermats_list = list(playermats)
        max_horses = self.playermat_set.all().aggregate(
            models.Max('horses'))['horses__max']
        max_horse_players = self.playermat_set.filter(horses=max_horses)

        # first turn, no player order set yet, no horses
        # this is ok for INITIAL drat but should be updated to dice rolling to
        # match game rules expectation
        if self.current_turn == 1:
            if self.is_solo_game:
                ai_playermat = playermats.get(player=JoanAI.get_user_joan())
                ai_idx = playermats_list.index(ai_playermat)
                player_one_idx = int(not ai_idx)
            else:
                player_one_idx = playermats_list.index(random.choice(playermats))

        # check for clear max_horses
        elif max_horse_players.count() == 1:
            player_one = max_horse_players[0]
            player_one_idx = playermats_list.index(player_one)

        else:
            # no max horses, simply increment the player_order
            player_one = playermats.get(player_order=2)
            player_one_idx = playermats_list.index(player_one)

        # reorder playermats so that player_one_idx is first, but still
        # 'incremental' ids
        reordered_mats = playermats[player_one_idx:] + \
            playermats[:player_one_idx]

        initial_order = 1
        for playermat in reordered_mats:
            # initial turn, just go clockwise
            playermat.player_order = initial_order
            playermat.save()
            initial_order += 1
        return

    def get_current_player_playermat(self):
        return self.playermat_set.get(player=self.current_player)

    def add_dice_to_world(self, die_dict):
        if not self.gather_dice:
            self.gather_dice = {}
        for resource_type, die_faces_list in die_dict.items():
            self.gather_dice[resource_type] = self.gather_dice.get(resource_type, []) + die_faces_list
        self.save()
