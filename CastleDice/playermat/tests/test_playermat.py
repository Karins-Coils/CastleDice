from django.contrib.auth.models import User
from django.test import TestCase

from CastleDice.common.globals import TURN
from CastleDice.game.models import Game
from ..models import PlayerMat


class TestPlayerMat(TestCase):
    def setUp(self):
        self.user = User(
            email="test@this.com", username="test_user", password="cherries"
        )
        self.user.save()
        self.user2 = User(
            email="test2@this.com", username="test_user2", password="cherrimoya"
        )
        self.user2.save()

        self.user3 = User(
            email="test3@this.com", username="test_user3", password="queen-anne"
        )
        self.user3.save()

    def create_one_playermat_game(self):
        game = Game()
        game.save()
        playermat = PlayerMat(game=game, player=self.user)
        playermat.save()

        return playermat

    def create_two_playermat_game(self):
        game = Game()
        game.save()
        playermat = PlayerMat(game=game, player=self.user)
        playermat.save()

        playermat2 = PlayerMat(game=game, player=self.user2)
        playermat2.save()

        return playermat

    def create_three_playermat_game(self):
        game = Game()
        game.save()

        playermat = PlayerMat(game=game, player=self.user)
        playermat.save()

        playermat2 = PlayerMat(game=game, player=self.user2)
        playermat2.save()

        playermat3 = PlayerMat(game=game, player=self.user3)
        playermat3.save()

        return playermat

    def test_get_player_choice_extra_dice(self):
        playermat = self.create_one_playermat_game()
        playermat.game.current_turn = 1
        playermat.game.save()

        self.assertEqual(
            playermat.get_player_choice_extra_dice(),
            TURN[playermat.game.current_turn]["no_choices"],
        )
