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
    def setUp(self):
        super().setUp()
        self.playermat = self.create_base_playermat()

    def create_base_playermat(self) -> PlayerMat:
        game = self.create_one_player_game()
        game.advance_turn()

        return game.playermat_set.first()


class TestPlayerMatGetPlayerChoiceExtraDice(BasePlayerMatTest):
    def test_get_player_choice_extra_dice(self):
        self.assertEqual(
            self.playermat.get_player_choice_extra_dice(), FirstTurn.number_of_choices
        )


class TestPlayerMatAddResource(BasePlayerMatTest):
    def test_add_resource_wood(self):
        self.playermat.add_resource(ResourceType.WOOD, 3)

        self.assertEqual(self.playermat.wood, 3)

    def test_add_resource_stone_default_value(self):
        self.playermat.add_resource(ResourceType.STONE)
        self.assertEqual(self.playermat.stone, 1)
        self.assertEqual(self.playermat.get_resource_count(ResourceType.STONE), 1)

        self.playermat.add_resource(ResourceType.STONE)
        self.assertEqual(self.playermat.stone, 2)
        self.assertEqual(self.playermat.get_resource_count(ResourceType.STONE), 2)

    def test_add_resource_hits_max(self):
        self.playermat.add_resource(ResourceType.LAND, 8)

        self.assertEqual(self.playermat.land, 8)

        # add past the max stops at the max
        self.playermat.add_resource(
            ResourceType.LAND, (GameConstants.MAX_RESOURCES - 8) + 4
        )
        self.assertEqual(self.playermat.land, GameConstants.MAX_RESOURCES)


class TestPlayerMatRemoveResource(BasePlayerMatTest):
    def test_remove_gold_default_value(self):
        self.playermat.add_resource(ResourceType.GOLD, 3)
        self.assertEqual(self.playermat.gold, 3)
        self.assertEqual(self.playermat.get_resource_count(ResourceType.GOLD), 3)

        self.playermat.remove_resource(ResourceType.GOLD)
        self.assertEqual(self.playermat.gold, 2)
        self.assertEqual(self.playermat.get_resource_count(ResourceType.GOLD), 2)

    def test_remove_iron(self):
        self.playermat.add_resource(ResourceType.IRON, 5)
        self.assertEqual(self.playermat.iron, 5)

        self.playermat.remove_resource(ResourceType.IRON, 3)
        self.assertEqual(self.playermat.iron, 2)

    def test_remove_below_zero(self):
        self.playermat.add_resource(ResourceType.IRON, 2)
        self.assertEqual(self.playermat.iron, 2)

        self.playermat.remove_resource(ResourceType.IRON, 4)
        self.assertEqual(self.playermat.iron, 0)


class TestPlayerMatAddRemoveVillager(BasePlayerMatTest):
    def test_add_barbarian(self):
        assert self.playermat.barbarians == 0

        self.playermat.add_barbarian()
        assert self.playermat.barbarians == 1

        self.playermat.add_barbarian(3)
        assert self.playermat.barbarians == 4

    def test_add_villager__barbarian(self):
        assert self.playermat.barbarians == 0
        self.playermat.add_villager(VillagerType.BARBARIAN, 3)

        assert self.playermat.barbarians == 3
        self.playermat.add_barbarian(2)
        assert self.playermat.barbarians == 5

    def test_add_villager__merchant_farmer(self):
        for villager in (VillagerType.MERCHANT, VillagerType.FARMER):
            attr_name = f"{villager.name.lower()}s"
            assert getattr(self.playermat, attr_name) == 0

            self.playermat.add_villager(villager)
            assert getattr(self.playermat, attr_name) == 1

            # anything that would make it more than 3 will error
            with self.assertRaises(VillagerMaxedOutError):
                self.playermat.add_villager(villager, 3)

            self.playermat.add_villager(villager, 2)
            assert getattr(self.playermat, attr_name) == 3

            # anything that would make it more than 3 will error
            with self.assertRaises(VillagerMaxedOutError):
                self.playermat.add_villager(villager)

            # reset and try with simple wrapper
            setattr(self.playermat, attr_name, 0)
            add_func = getattr(self.playermat, f"add_{villager.name.lower()}")
            add_func()
            assert getattr(self.playermat, attr_name) == 1

            with self.assertRaises(VillagerMaxedOutError):
                add_func(3)

            add_func(2)
            assert getattr(self.playermat, attr_name) == 3

    def test_add_worker(self):
        assert self.playermat.workers_mat.total == 0

        self.playermat.add_worker()
        assert self.playermat.workers_mat.total == 1

        with self.assertRaises(VillagerMaxedOutError):
            self.playermat.add_worker(5)

        self.playermat.add_worker(2)
        assert self.playermat.workers_mat.total == 3

        with self.assertRaises(InvalidResourceForVillagerError):
            assert self.playermat.workers_mat.stone
            self.playermat.add_worker(resource=ResourceType.STONE)

        assert self.playermat.workers_mat.iron is False
        self.playermat.add_worker(resource=ResourceType.IRON)
        assert self.playermat.workers_mat.iron
        assert self.playermat.workers_mat.total == 4

    def test_add_guard(self):
        assert self.playermat.guards_mat.total == 0

        # short way
        assert self.playermat.guards_mat.stone is False
        self.playermat.add_guard(ResourceType.STONE)
        assert self.playermat.guards_mat.total == 1
        assert self.playermat.guards_mat.stone

        with self.assertRaises(InvalidResourceForVillagerError):
            self.playermat.add_guard(ResourceType.STONE)

        # Long way
        assert self.playermat.guards_mat.gold is False
        self.playermat.add_villager(VillagerType.GUARD, to_resource=ResourceType.GOLD)
        assert self.playermat.guards_mat.gold

        with self.assertRaises(InvalidResourceForVillagerError):
            self.playermat.add_villager(
                VillagerType.GUARD, to_resource=ResourceType.GOLD
            )

        with self.assertRaises(MissingGuardResourceError):
            self.playermat.add_villager(VillagerType.GUARD)


class TestPlayerMatResourcePeople(BasePlayerMatTest):
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
