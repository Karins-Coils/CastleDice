import random

from castledice.common.constants import GameConstants, ResourceType, VillagerType
from castledice.game.tests import utils
from castledice.game.turns import FirstTurn

from ..exceptions import (
    InvalidResourceForVillagerError,
    MissingGuardResourceError,
    NoMoreOfVillagerError,
    UnknownVillagerTypeError,
    VillagerMaxedOutError,
    VillagerTypeCannotHaveResourcesError,
    VillagerTypeMustHaveResourcesError,
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
    def test_add_remove_unknown(self):
        with self.assertRaises(UnknownVillagerTypeError):
            self.playermat.add_villager(ResourceType.WOOD, 2)

        with self.assertRaises(UnknownVillagerTypeError):
            self.playermat.remove_villager(ResourceType.WOOD)

    def test_add_remove_barbarian(self):
        assert self.playermat.barbarians == 0

        self.playermat.add_barbarian()
        assert self.playermat.barbarians == 1

        self.playermat.add_barbarian(3)
        assert self.playermat.barbarians == 4

        self.playermat.remove_barbarian()
        assert self.playermat.barbarians == 3

        self.playermat.remove_barbarian(2)
        assert self.playermat.barbarians == 1

        # confirm we don't remove past the minimum
        self.playermat.remove_barbarian(4)
        assert self.playermat.barbarians == 0

    def test_add_remove_villager__barbarian(self):
        assert self.playermat.barbarians == 0

        self.playermat.add_villager(VillagerType.BARBARIAN)
        assert self.playermat.barbarians == 1

        self.playermat.add_villager(VillagerType.BARBARIAN, 4)
        assert self.playermat.barbarians == 5

        self.playermat.remove_villager(VillagerType.BARBARIAN)
        assert self.playermat.barbarians == 4

        self.playermat.remove_villager(VillagerType.BARBARIAN, 6)
        assert self.playermat.barbarians == 0

    def test_add_remove_villager__merchant_farmer(self):
        for villager in (VillagerType.MERCHANT, VillagerType.FARMER):
            attr_name = f"{villager.name.lower()}s"
            assert getattr(self.playermat, attr_name) == 0

            # - Long way tests - #
            # --- Addition --- #
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

            # --- Subtraction --- #
            self.playermat.remove_villager(villager)
            assert getattr(self.playermat, attr_name) == 2

            self.playermat.remove_villager(villager, 2)
            assert getattr(self.playermat, attr_name) == 0

            with self.assertRaises(NoMoreOfVillagerError):
                self.playermat.remove_villager(villager)

            # - Simple wrapper - #
            # --- Addition --- #
            # add_func -> self.playermat.add_farmer or self.playermat.add_merchant
            add_func = getattr(self.playermat, f"add_{villager.name.lower()}")

            add_func()
            assert getattr(self.playermat, attr_name) == 1

            with self.assertRaises(VillagerMaxedOutError):
                add_func(3)

            add_func(2)
            assert getattr(self.playermat, attr_name) == 3

            # --- Subtraction --- #
            # add_func -> self.playermat.remove_farmer or self.playermat.remove_merchant
            remove_func = getattr(self.playermat, f"remove_{villager.name.lower()}")

            remove_func()
            assert getattr(self.playermat, attr_name) == 2

            remove_func(2)
            assert getattr(self.playermat, attr_name) == 0

            with self.assertRaises(NoMoreOfVillagerError):
                remove_func()

    def test_add_worker(self):
        # - Short way - #
        # --- Addition --- #
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

        # --- Subtraction --- #
        assert self.playermat.workers_mat.wood
        self.playermat.remove_worker(resource=ResourceType.WOOD)
        assert self.playermat.workers_mat.wood is False

        with self.assertRaises(InvalidResourceForVillagerError):
            self.playermat.remove_worker(resource=ResourceType.LAND)

        self.playermat.remove_worker(resource=ResourceType.GOLD)

        # - Long way - #
        # --- Addition --- #
        # should add to lowest spot that is empty
        assert self.playermat.workers_mat.wood is False
        self.playermat.add_villager(VillagerType.WORKER)
        assert self.playermat.workers_mat.wood
        assert self.playermat.workers_mat.total == 3

        with self.assertRaises(InvalidResourceForVillagerError):
            assert self.playermat.workers_mat.stone
            self.playermat.add_villager(
                VillagerType.WORKER, to_resource=ResourceType.STONE
            )

        self.playermat.add_villager(VillagerType.WORKER, 2)
        assert self.playermat.workers_mat.total == 5

        with self.assertRaises(VillagerMaxedOutError):
            self.playermat.add_villager(VillagerType.WORKER)

        # --- Subtraction --- #
        with self.assertRaises(InvalidResourceForVillagerError):
            assert self.playermat.remove_villager(VillagerType.WORKER)

        with self.assertRaises(InvalidResourceForVillagerError):
            assert self.playermat.remove_villager(VillagerType.WORKER, 3)

        assert self.playermat.workers_mat.land
        self.playermat.remove_villager(
            VillagerType.WORKER, from_resource=ResourceType.LAND
        )
        assert self.playermat.workers_mat.land is False

    def test_add_guard(self):
        assert self.playermat.guards_mat.total == 0

        # - Short way - #
        # --- Addition --- #
        assert self.playermat.guards_mat.stone is False
        self.playermat.add_guard(ResourceType.STONE)
        assert self.playermat.guards_mat.total == 1
        assert self.playermat.guards_mat.stone

        with self.assertRaises(InvalidResourceForVillagerError):
            self.playermat.add_guard(ResourceType.STONE)
        # --- Subtraction --- #
        with self.assertRaises(InvalidResourceForVillagerError):
            self.playermat.remove_guard(ResourceType.GOLD)

        self.playermat.remove_guard(ResourceType.STONE)
        assert self.playermat.guards_mat.stone is False

        # - Long way - #
        # --- Addition --- #
        assert self.playermat.guards_mat.gold is False
        self.playermat.add_villager(VillagerType.GUARD, to_resource=ResourceType.GOLD)
        assert self.playermat.guards_mat.gold

        with self.assertRaises(InvalidResourceForVillagerError):
            self.playermat.add_villager(
                VillagerType.GUARD, to_resource=ResourceType.GOLD
            )

        with self.assertRaises(MissingGuardResourceError):
            self.playermat.add_villager(VillagerType.GUARD)

        # --- Subtraction --- #
        with self.assertRaises(InvalidResourceForVillagerError):
            self.playermat.remove_villager(VillagerType.GUARD)

        with self.assertRaises(InvalidResourceForVillagerError):
            self.playermat.remove_villager(
                VillagerType.GUARD, from_resource=ResourceType.LAND
            )

        self.playermat.remove_villager(
            VillagerType.GUARD, from_resource=ResourceType.GOLD
        )
        assert self.playermat.guards_mat.gold is False

        with self.assertRaises(NoMoreOfVillagerError):
            self.playermat.remove_villager(
                VillagerType.GUARD, from_resource=ResourceType.GOLD
            )


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

    def test_convert_villager__requires_resource_to_be_included(self):
        self.playermat.merchants = 2
        self.playermat.save()
        self.playermat.workers_mat.add_to_resource(ResourceType.WOOD)
        self.playermat.guards_mat.add_to_resource(ResourceType.WOOD)

        invalid_kwargs_for_guard = [
            # Guard requires a resource
            dict(
                current_villager=VillagerType.GUARD, new_villager=VillagerType.MERCHANT
            ),
            dict(
                current_villager=VillagerType.MERCHANT, new_villager=VillagerType.GUARD
            ),
            dict(
                current_villager=VillagerType.WORKER,
                current_resource=ResourceType.WOOD,
                new_villager=VillagerType.GUARD,
            ),
            dict(
                current_villager=VillagerType.GUARD,
                new_villager=VillagerType.WORKER,
                new_resource=ResourceType.WOOD,
            ),
        ]
        invalid_kwargs_for_worker = [
            # Worker requires a resource
            dict(
                current_villager=VillagerType.WORKER, new_villager=VillagerType.MERCHANT
            ),
            dict(
                current_villager=VillagerType.MERCHANT, new_villager=VillagerType.WORKER
            ),
            dict(
                current_villager=VillagerType.GUARD,
                current_resource=ResourceType.WOOD,
                new_villager=VillagerType.WORKER,
            ),
            dict(
                current_villager=VillagerType.WORKER,
                new_villager=VillagerType.GUARD,
                new_resource=ResourceType.WOOD,
            ),
        ]
        for village_name, kwargs_list in [
            ("GUARD", invalid_kwargs_for_guard),
            ("WORKER", invalid_kwargs_for_worker),
        ]:
            for kwargs in kwargs_list:
                with self.subTest(villager_name=village_name, kwargs=kwargs):
                    with self.assertRaisesRegex(
                        InvalidResourceForVillagerError, village_name
                    ):
                        self.playermat.convert_villager(**kwargs)

    def test_convert_villager__villager_not_allowed(self):
        self.playermat.merchants = 3
        self.playermat.farmers = 0
        self.playermat.save()

        # current is empty
        with self.assertRaises(NoMoreOfVillagerError):
            self.playermat.convert_villager(VillagerType.FARMER, VillagerType.MERCHANT)

        self.playermat.farmers = 2
        self.playermat.save()
        # new has no more room
        with self.assertRaises(VillagerMaxedOutError):
            self.playermat.convert_villager(VillagerType.FARMER, VillagerType.MERCHANT)

        self.playermat.workers_mat.add_to_resource(ResourceType.WOOD)
        self.playermat.guards_mat.add_to_resource(ResourceType.IRON)
        # current has no villager w/ resource there
        with self.assertRaises(NoMoreOfVillagerError):
            self.playermat.convert_villager(
                current_villager=VillagerType.WORKER,
                current_resource=ResourceType.STONE,
                new_villager=VillagerType.FARMER,
            )
        # new already has villager her
        with self.assertRaises(InvalidResourceForVillagerError):
            self.playermat.convert_villager(
                current_villager=VillagerType.WORKER,
                current_resource=ResourceType.WOOD,
                new_villager=VillagerType.GUARD,
                new_resource=ResourceType.IRON,
            )

    def test_convert_villager__success(self):
        self.playermat.merchants = 2
        self.playermat.farmers = 1
        self.playermat.save()
        self.playermat.workers_mat.add_to_resource(ResourceType.WOOD)
        self.playermat.guards_mat.add_to_resource(ResourceType.IRON)

        # try moving from non-resource to resource
        assert self.playermat.workers_mat.stone is False
        self.playermat.convert_villager(
            current_villager=VillagerType.MERCHANT,
            new_villager=VillagerType.WORKER,
            new_resource=ResourceType.STONE,
        )
        assert self.playermat.workers_mat.stone
        assert self.playermat.merchants == 1
        assert self.playermat.workers_mat.total == 2

        # try moving from resource to non-resource
        self.playermat.convert_villager(
            current_villager=VillagerType.GUARD,
            current_resource=ResourceType.IRON,
            new_villager=VillagerType.FARMER,
        )
        assert self.playermat.farmers == 2
        assert self.playermat.guards_mat.iron is False
        assert self.playermat.guards_mat.total == 0

        # try moving from resource to resource on same villager
        self.playermat.convert_villager(
            current_villager=VillagerType.WORKER,
            current_resource=ResourceType.WOOD,
            new_villager=VillagerType.WORKER,
            new_resource=ResourceType.GOLD,
        )
        assert self.playermat.workers_mat.wood is False
        assert self.playermat.workers_mat.gold
        assert self.playermat.workers_mat.total == 2

    def test_get_mat_for_villager(self):
        for villager in (VillagerType.MERCHANT, VillagerType.FARMER):
            with self.assertRaises(VillagerTypeMustHaveResourcesError):
                self.playermat.get_mat_for_villager(villager)

        for villager in (VillagerType.GUARD, VillagerType.WORKER):
            villager_mat = self.playermat.get_mat_for_villager(villager)
            assert villager_mat.type == villager

    def test_get_villager_count(self):
        self.playermat.barbarians = 3
        self.playermat.merchants = 1
        self.playermat.farmers = 2
        self.playermat.save()

        for villager in (VillagerType.GUARD, VillagerType.WORKER):
            with self.assertRaises(VillagerTypeCannotHaveResourcesError):
                self.playermat.get_villager_count(villager)

        for villager, expected_count in [
            (VillagerType.MERCHANT, 1),
            (VillagerType.FARMER, 2),
            (VillagerType.BARBARIAN, 3),
        ]:
            villager_count = self.playermat.get_villager_count(villager)
            assert villager_count == expected_count
