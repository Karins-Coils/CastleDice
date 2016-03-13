from django.test import TestCase
from game.models import Game
from playermat.models import PlayerMat
from django.contrib.auth.models import User
from CD_globals import WOOD, STONE, GOLD, LAND, IRON, TURN


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
