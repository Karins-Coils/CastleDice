import random

from annoying.fields import JSONField
from django.conf import settings
from django.db import models

from .solo_ai import JoanAI
from .turns import Turn


# in progress rewrite
class Game(models.Model):
    is_solo_game = models.BooleanField(default=False)
    # prevent backwards relation with related_name='+'
    current_player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )
    # prevent backwards relation with related_name='+', as the Turn has a game already linked
    current_turn = models.ForeignKey(
        "GameTurn", on_delete=models.SET_NULL, null=True, related_name="+", default=None
    )
    current_phase = models.PositiveSmallIntegerField(default=1)
    choice_dice_bank = JSONField(
        blank=True, null=True, default=[]
    )  # list of die types available
    gather_dice_bank = JSONField(
        blank=True, null=True, default=[]
    )  # list of already rolled dice available

    def setup_choice_dice_for_turn(self):
        """
        Based on the current turn, setup the choice dice bank, and put the given dice
        into each player's pool
        """
        turn = Turn(self.current_turn.turn_no)
        given_dice = turn.create_player_choice_dice_for_turn()

        # setup base choice die for all players with initial given set
        for playermat in self.playermat_set.all():
            playermat.choice_dice = given_dice
            playermat.save()

        self.dice_bank = turn.create_dice_bank_for_turn(self.playermat_set.count())
        self.save()

    def advance_turn(self):
        """
        Setup or reset the turn based values tracked in the Game.
        Also advance the turn number, and determine the new player order.
        """
        # TODO: custom logic to advance turn & reset base values
        # TODO: confirm barbarians phase completed

        # advance the turn, creating a new GameTurn
        if self.current_turn:
            self.current_turn = GameTurn.initialize_turn(
                self, self.current_turn.turn_no + 1
            )
        else:
            self.current_turn = GameTurn.initialize_turn(self, 1)

        # set player order on players
        self.determine_player_order()

        # get current player based on new player order
        self.current_player = self.playermat_set.get(player_order=1).player

        # clear dice banks
        self.choice_dice_bank = None
        self.gather_dice_bank = None

        # reset the phase
        self.current_phase = 1

        self.save()

    def advance_phase(self):
        """
        Update the current phase number to be the next phase.  Also advance the current player
        """
        # TODO: custom logic to check if all players have had their turn
        # or other conditions met (gathered all dice, etc)

        self.current_phase += 1
        # reset first player of the phase back to first player
        self.current_player = self.playermat_set.get(player_order=1).player
        self.save()

    def advance_current_player(self):
        """
        Based on game.current_player & each playermat.player_order,
        set game.current_player to the next player in order
        Used during a turn, after player_order has already been set.
        """
        # get the current player's order
        current_player_order = self.playermat_set.get(
            player=self.current_player
        ).player_order

        # if the player_order is equal to the total number of players,
        # go back to the first player
        if current_player_order == self.playermat_set.count():
            self.current_player = self.playermat_set.get(player_order=1).player

        # else get the player with the next highest player_order
        else:
            self.current_player = self.playermat_set.get(
                player_order=current_player_order + 1
            ).player

        self.save()

    def determine_player_order(self):
        playermats = self.playermat_set.all().order_by("id")
        playermats_list = list(playermats)
        max_horses = self.playermat_set.all().aggregate(models.Max("horses"))[
            "horses__max"
        ]
        max_horse_players = self.playermat_set.filter(horses=max_horses)

        # first turn, no player order set yet, no horses
        # this is ok for INITIAL drat but should be updated to dice rolling to
        # match game rules expectation
        if self.current_turn.turn_no == 1:
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
        reordered_mats = playermats[player_one_idx:] + playermats[:player_one_idx]

        initial_order = 1
        for playermat in reordered_mats:
            # initial turn, just go clockwise
            playermat.player_order = initial_order
            playermat.save()
            initial_order += 1
        return

    def get_current_player_playermat(self):
        return self.playermat_set.get(player=self.current_player)

    # def add_dice_to_world(self, die_dict):
    #     if not self.world_pool_dice:
    #         self.world_pool_dice = {}
    #     for resource_type, die_faces_list in die_dict.items():
    #         self.world_pool_dice[resource_type] = (
    #             self.world_pool_dice.get(resource_type, []) + die_faces_list
    #         )
    #     self.save()


class GameTurn(models.Model):
    """The turn details for a specific turn"""

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="turns")
    turn_no = models.PositiveSmallIntegerField(default=1)
    # prevent backwards relation with related_name='+'
    first_player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )
    # prevent backwards relation with related_name='+'
    pork_chop_used_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )

    @classmethod
    def initialize_turn(cls, game: Game, turn_no: int = 1) -> "GameTurn":
        """Create a row in the game_turns table connected to the supplied game for the first turn

        :param game:
        :type game: Game
        :param turn_no:
        :type: int:
        :return:
        :rtype: GameTurn
        """
        return cls.objects.create(game=game, turn_no=turn_no)
