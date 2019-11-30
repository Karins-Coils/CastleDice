from CastleDice.common.constants import GameConstants
from CastleDice.common.constants import ResourceType
from CastleDice.game.tests import utils
from CastleDice.game.turns import FirstTurn
from ..models import PlayerMat


class BasePlayerMatTest(utils.BaseGameTest):
    def create_base_playermat(self) -> PlayerMat:
        game = self.create_one_player_game()
        game.advance_turn()

        return game.playermat_set.first()


class TestPlayerMatGetPlayerChoiceExtraDice(BasePlayerMatTest):
    def test_get_player_choice_extra_dice(self):
        playermat = self.create_base_playermat()

        self.assertEqual(
            playermat.get_player_choice_extra_dice(), FirstTurn.number_of_choices
        )


class TestPlayerMatAddResource(BasePlayerMatTest):
    def test_add_resource_wood(self):
        playermat = self.create_base_playermat()

        playermat.add_resource(ResourceType.WOOD, 3)

        self.assertEqual(playermat.wood, 3)

    def test_add_resource_stone_default_value(self):
        playermat = self.create_base_playermat()

        playermat.add_resource(ResourceType.STONE)

        self.assertEqual(playermat.stone, 1)

    def test_add_resource_hits_max(self):
        playermat = self.create_base_playermat()

        playermat.add_resource(ResourceType.LAND, 8)

        self.assertEqual(playermat.land, 8)

        # add past the max stops at the max
        playermat.add_resource(ResourceType.LAND, (GameConstants.MAX_RESOURCES - 8) + 4)
        self.assertEqual(playermat.land, GameConstants.MAX_RESOURCES)


class TestPlayerMatRemoveResource(BasePlayerMatTest):
    def test_remove_gold_default_value(self):
        playermat = self.create_base_playermat()

        playermat.add_resource(ResourceType.GOLD, 3)
        self.assertEqual(playermat.gold, 3)

        playermat.remove_resource(ResourceType.GOLD)
        self.assertEqual(playermat.gold, 2)

    def test_remove_iron(self):
        playermat = self.create_base_playermat()

        playermat.add_resource(ResourceType.IRON, 5)
        self.assertEqual(playermat.iron, 5)

        playermat.remove_resource(ResourceType.IRON, 3)
        self.assertEqual(playermat.iron, 2)

    def test_remove_below_zero(self):
        playermat = self.create_base_playermat()

        playermat.add_resource(ResourceType.IRON, 2)
        self.assertEqual(playermat.iron, 2)

        playermat.remove_resource(ResourceType.IRON, 4)
        self.assertEqual(playermat.iron, 0)
