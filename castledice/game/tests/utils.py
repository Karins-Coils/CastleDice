from typing import Dict
from typing import List

from django.contrib.auth.models import User
from django.test import TestCase

from castledice.common.constants import ResourceType
from castledice.game.models import Game
from castledice.game.solo_ai import JoanAI
from castledice.playermat.models import PlayerMat


class BaseGameTest(TestCase):
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

        # create Joan
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

    def create_expected_die_list(
        self, resource_count_dict: Dict[ResourceType, int]
    ) -> List[ResourceType]:
        die_list = []
        for resource, count in resource_count_dict.items():
            die_list.extend([resource] * count)
        return die_list
