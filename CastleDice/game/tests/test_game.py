from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase

from CastleDice.common.globals import GOLD
from CastleDice.common.globals import IRON
from CastleDice.common.globals import LAND
from CastleDice.common.globals import STONE
from CastleDice.common.globals import TURN
from CastleDice.common.globals import WOOD
from CastleDice.game.models import Game
from CastleDice.game.solo_ai import JoanAI
from CastleDice.playermat.models import PlayerMat


class TestGameModel(TestCase):

    def setUp(self):
        self.user = User(email="test@this.com",
                         username="test_user",
                         password="cherries")
        self.user.save()
        self.user2 = User(email="test2@this.com",
                          username="test_user2",
                          password="cherrimoya")
        self.user2.save()

        self.user3 = User(email="test3@this.com",
                          username="test_user3",
                          password="queen-anne")
        self.user3.save()

        JoanAI.get_user_joan()

    def create_one_player_game(self):
        game = Game()
        game.save()
        playermat = PlayerMat(game=game, player=self.user)
        playermat.save()

        return game

    def create_two_player_game(self):
        game = Game()
        game.save()
        playermat = PlayerMat(game=game, player=self.user)
        playermat.save()

        playermat2 = PlayerMat(game=game, player=self.user2)
        playermat2.save()

        return game

    def create_three_player_game(self):
        game = Game()
        game.save()

        playermat = PlayerMat(game=game, player=self.user)
        playermat.save()

        playermat2 = PlayerMat(game=game, player=self.user2)
        playermat2.save()

        playermat3 = PlayerMat(game=game, player=self.user3)
        playermat3.save()

        return game

    def test_player_order_turn_one_multi(self):
        game = self.create_three_player_game()
        game.current_turn = 1
        game.save()

        # confirm that beginning orders are all the default 0
        player_orders = set([playermat.player_order
                             for playermat in game.playermat_set.all()])
        self.assertEqual([0], list(player_orders), "Player orders were not "
                         "initialized at 0 as expected")

        # set the player order in a turn 1 game (random as 3rd player),
        # best scenario to check for consistency
        with mock.patch('random.choice', side_effect=lambda seq: seq[2]):
            game.determine_player_order()

        # confirm that we have [1, 2, 3] as orders
        player_orders = set([playermat.player_order
                             for playermat in game.playermat_set.all()])
        self.assertEqual([1, 2, 3], list(player_orders), "An unexpected player"
                         " order was assigned")

        # find the lowest playermat id
        playermats_by_player_order = \
            game.playermat_set.all().order_by('player_order')
        playermat_lowest_id = playermats_by_player_order.order_by('id')[0]
        playermat_lowest_id_idx = \
            list(playermats_by_player_order).index(playermat_lowest_id)

        # locate its index in the player order list, then re-splice list
        playermats_by_player_id = \
            playermats_by_player_order[playermat_lowest_id_idx:] + \
            playermats_by_player_order[:playermat_lowest_id_idx]
        playermats_player_ids = [playermat.id
                                 for playermat in playermats_by_player_id]

        # confirm it incremented the player_order by id's
        self.assertEqual(sorted(playermats_player_ids),
                         playermats_player_ids, "The player order did not "
                         "implement 'clockwise' player order iteration.")

    def test_player_order_turn_one_solo(self):
        game = self.create_one_player_game()
        game.current_turn = 1
        game.save()

        game.determine_player_order()

        # confirm that first player is NOT joan
        joan_player = JoanAI.get_user_joan()
        player_one = game.playermat_set.filter(player_order=1)[0]
        self.assertNotEqual(player_one, joan_player)

    def test_player_order_turn_six_max_horses(self):
        game = self.create_three_player_game()
        game.current_turn = 1
        game.save()

        # set initial turn order as 3rd player first
        with mock.patch('random.choice', side_effect=lambda seq: seq[2]):
            game.determine_player_order()

        # setup the 3 playermats with horses, with player_order = 3 as winner
        horses = 1
        playermats = game.playermat_set.all().order_by('player_order')
        for playermat in playermats:
            playermat.horses = horses
            playermat.save()
            horses += 1

        # 3rd player before should become player 1
        third_player = playermats[2]

        # set current_turn to not first turn
        game.current_turn = 6

        game.determine_player_order()
        first_player = game.playermat_set.all().order_by('player_order')[0]

        # confirm that previous 3rd player (with max horses) is now first
        self.assertEqual(third_player.id, first_player.id, "Player order not "
                         "choosing player with max horses as expected.")

    def test_player_order_turn_six_horses_tied(self):
        game = self.create_three_player_game()
        game.current_turn = 1
        game.save()

        # set initial turn order as 3rd player first
        with mock.patch('random.choice', side_effect=lambda seq: seq[2]):
            game.determine_player_order()

        # setup the 3 playermats to have tied horses with 2 players
        horses = 4
        playermats = game.playermat_set.all().order_by('player_order')
        # set first two players as 'tied'
        for playermat in playermats[:2]:
            playermat.horses = horses
            playermat.save()

        # 2nd player before will become player 1
        second_player = playermats[1]

        # set current_turn to not first turn
        game.current_turn = 6

        game.determine_player_order()
        first_player = game.playermat_set.all().order_by('player_order')[0]

        # confirm that previous 3rd player (with max horses) is now first
        self.assertEqual(second_player.id, first_player.id, "Player order not "
                         "choosing player in clockwise when horses tied.")

    def test_setup_choice_dice_for_turn_one_player(self):
        # one playermat, minus Turn 1 choice dice
        choice_pool_count = {
            WOOD:  12,  # minus the 2 given wood
            STONE: 12,  # minus the 2 given stone
            GOLD:  12,  # minus the 1 given gold
            LAND:  11,
            IRON:  11
        }
        game = self.create_one_player_game()
        game.current_turn = 1
        game.setup_choice_dice_for_turn()

        # confirm only playermat in the set has base choice dice
        playermat = game.playermat_set.get()
        self.assertEqual(playermat.choice_dice,
                         TURN[game.current_turn]['given_dice'])
        self.assertEqual(game.choice_dice, choice_pool_count)

    def test_setup_choice_dice_for_turn_two_player(self):
        # minus Turn 2 choice dice * two playermat
        choice_pool_count = {
            WOOD:  12,  # minus the 1 given wood * 2
            STONE: 12,  # minus the 1 given stone * 2
            GOLD:  9,  # minus the 2 given gold * 2
            LAND:  11,
            IRON:  11
        }
        game = self.create_two_player_game()
        game.current_turn = 2
        game.setup_choice_dice_for_turn()

        # confirm all playermats in the set have base choice dice
        for playermat in game.playermat_set.all():
            self.assertEqual(playermat.choice_dice,
                             TURN[game.current_turn]['given_dice'])

        self.assertEqual(game.choice_dice, choice_pool_count)

    def test_setup_choice_dice_for_turn_three_player(self):
        # minus Turn 3 choice dice * three playermat
        choice_pool_count = {
            WOOD:  5,  # minus the 3 given wood * 3
            STONE: 11,  # minus the 1 given stone * 3
            GOLD:  10,  # minus the 1 given gold * 3
            LAND:  11,
            IRON:  11
        }
        game = self.create_three_player_game()
        game.current_turn = 3
        game.setup_choice_dice_for_turn()

        # confirm all playermats in the set have base choice dice
        for playermat in game.playermat_set.all():
            self.assertEqual(playermat.choice_dice,
                             TURN[game.current_turn]['given_dice'])

        self.assertEqual(game.choice_dice, choice_pool_count)
