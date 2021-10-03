import random

from castledice.common.constants import GameConstants, ResourceType, VillagerType
from castledice.game.tests import utils
from castledice.game.turns import FirstTurn

from ..exceptions import (
    InvalidResourceForVillagerError,
    MissingGuardResourceError,
    NoMoreOfVillagerError,
    VillagerMaxedOutError,
)
from ..models import PlayerMat, PlayerMatResourcePeople


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


class TestPlayerMatResourcePeople(BasePlayerMatTest):
    def setUp(self):
        super().setUp()
        self.playermat = self.create_base_playermat()

    def test_add_single_guard(self):
        playermat_resource_guard = PlayerMatResourcePeople.objects.create(
            player_mat=self.playermat, type=VillagerType.GUARD
        )
        playermat_resource_guard.add_to_resource(ResourceType.LAND)
        self.assertTrue(playermat_resource_guard.land)
        self.assertEqual(playermat_resource_guard.total, 1)

        with self.assertRaises(InvalidResourceForVillagerError):
            playermat_resource_guard.add_to_resource(ResourceType.LAND)

        with self.assertRaises(MissingGuardResourceError):
            playermat_resource_guard.add_to_resource()

    def test_add_worker(self):
        playermat_resource_worker = PlayerMatResourcePeople.objects.create(
            player_mat=self.playermat, type=VillagerType.WORKER
        )
        # first one goes to wood, second one goes to stone, etc
        for idx, resource in enumerate(list(ResourceType)):
            # test self.has_resource
            self.assertFalse(playermat_resource_worker.has_resource(resource))

            playermat_resource_worker.add_to_resource()

            # test self.has_resource
            self.assertTrue(playermat_resource_worker.has_resource(resource))

            # test self.total
            self.assertEqual(playermat_resource_worker.total, idx + 1)

        # sixth time is an error -- no more space
        with self.assertRaises(VillagerMaxedOutError):
            playermat_resource_worker.add_to_resource()

    def test_add_beyond_max_guard(self):
        playermat_resource_guard = PlayerMatResourcePeople.objects.create(
            player_mat=self.playermat, type=VillagerType.GUARD
        )

        # add to all five resources - in random order
        resources = list(ResourceType)
        random.shuffle(resources)

        for resource in resources:
            playermat_resource_guard.add_to_resource(resource)

        # sixth time is an error -- no more space
        with self.assertRaises(VillagerMaxedOutError):
            playermat_resource_guard.add_to_resource()

    def test_remove_worker(self):
        playermat_resource_worker = PlayerMatResourcePeople.objects.create(
            player_mat=self.playermat, type=VillagerType.WORKER
        )

        # add to all five resources
        for _ in range(5):
            playermat_resource_worker.add_to_resource()

        assert playermat_resource_worker.total == 5

        # start removing - can be removed in any order
        resources = list(ResourceType)
        random.shuffle(resources)

        for idx, resource in enumerate(resources):
            assert playermat_resource_worker.total == 5 - idx
            assert playermat_resource_worker.has_resource(resource)
            playermat_resource_worker.remove_from_resource(resource)
            assert playermat_resource_worker.has_resource(resource) is False
            assert playermat_resource_worker.total == 5 - (idx + 1)

        # remove when none are left
        with self.assertRaises(NoMoreOfVillagerError):
            playermat_resource_worker.remove_from_resource(ResourceType.WOOD)

    def test_add_and_remove_guard(self):
        playermat_resource_guard = PlayerMatResourcePeople.objects.create(
            player_mat=self.playermat, type=VillagerType.GUARD
        )
        resource = ResourceType.IRON
        assert playermat_resource_guard.total == 0
        assert playermat_resource_guard.has_resource(resource) is False

        playermat_resource_guard.add_to_resource(resource)

        assert playermat_resource_guard.has_resource(resource)
        assert playermat_resource_guard.total == 1

        # try to remove an invalid resource
        with self.assertRaises(InvalidResourceForVillagerError):
            playermat_resource_guard.remove_from_resource(ResourceType.WOOD)

        playermat_resource_guard.remove_from_resource(resource)

        assert playermat_resource_guard.total == 0
        assert playermat_resource_guard.has_resource(resource) is False

        # remove when none are left
        with self.assertRaises(NoMoreOfVillagerError):
            playermat_resource_guard.remove_from_resource(resource)
