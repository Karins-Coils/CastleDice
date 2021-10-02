from unittest import mock

from castledice.common.constants import ResourceType

from ..models import Game, GameTurn
from ..solo_ai import JoanAI
from .utils import BaseGameTest


class TestGameModel(BaseGameTest):
    def test_create_game(self):
        game = Game()
        game.save()
        self.assertEqual(game, Game.objects.get(id=game.id))

    def test_advance_turn(self):
        game = self.create_two_player_game()
        # initialize the game state to the first turn
        game.advance_turn()

        self.assertEqual(game.current_turn.turn_no, 1)
        self.assertEqual(game.current_phase, 1)
        self.assertIsNone(game.choice_dice_bank)
        self.assertIsNone(game.gather_dice_bank)
        self.assertIsNotNone(game.current_player)

        # pretend to have some values
        game.choice_dice_bank = []
        game.gather_dice_bank = []
        game.current_phase = 5
        game.save()

        first_turn_player = game.current_player

        # advance to the second turn
        game.advance_turn()

        self.assertEqual(game.current_turn.turn_no, 2)
        self.assertEqual(game.current_phase, 1)
        self.assertIsNone(game.choice_dice_bank)
        self.assertIsNone(game.gather_dice_bank)
        self.assertNotEqual(game.current_player, first_turn_player)

    def test_advance_phase(self):
        game = self.create_two_player_game()
        # initialize the game state to the first turn
        game.advance_turn()

        self.assertEqual(game.current_phase, 1)
        self.assertIsNotNone(game.current_player)

        first_round_player = game.current_player

        # move the round to the next player, to simulate the game moving along
        game.advance_current_player()
        self.assertNotEqual(game.current_player, first_round_player)

        # advance to the next game phase
        game.advance_phase()
        self.assertEqual(game.current_phase, 2)
        # player should be the same as the original again
        self.assertEqual(game.current_player, first_round_player)

    def test_advance_current_player(self):
        game = self.create_three_player_game()
        # initialize the game state to the first turn
        game.advance_turn()

        first_player = game.playermat_set.get(player_order=1).player
        second_player = game.playermat_set.get(player_order=2).player
        third_player = game.playermat_set.get(player_order=3).player

        # current state, should be set to first player
        self.assertEqual(game.current_player, first_player)

        # advance the player
        game.advance_current_player()
        self.assertEqual(game.current_player, second_player)

        # advance the player again
        game.advance_current_player()
        self.assertEqual(game.current_player, third_player)

        # final advance should bring it back to the start (important for gather phase, etc)
        game.advance_current_player()
        self.assertEqual(game.current_player, first_player)

    def test_player_order_turn_one_multi(self):
        game = self.create_three_player_game()
        game.current_turn = GameTurn.initialize_turn(game)
        game.save()

        # confirm that beginning orders are all the default 0
        player_orders = set(
            [playermat.player_order for playermat in game.playermat_set.all()]
        )
        self.assertEqual(
            [0],
            list(player_orders),
            "Player orders were not " "initialized at 0 as expected",
        )

        # set the player order in a turn 1 game (random as 3rd player),
        # best scenario to check for consistency
        with mock.patch("random.choice", side_effect=lambda seq: seq[2]):
            game.determine_player_order()

        # confirm that we have [1, 2, 3] as orders
        player_orders = set(
            [playermat.player_order for playermat in game.playermat_set.all()]
        )
        self.assertEqual(
            [1, 2, 3], list(player_orders), "An unexpected player" " order was assigned"
        )

        # find the lowest playermat id
        playermats_by_player_order = game.playermat_set.all().order_by("player_order")
        playermat_lowest_id = playermats_by_player_order.order_by("id")[0]
        playermat_lowest_id_idx = list(playermats_by_player_order).index(
            playermat_lowest_id
        )

        # locate its index in the player order list, then re-splice list
        playermats_by_player_id = (
            playermats_by_player_order[playermat_lowest_id_idx:]
            + playermats_by_player_order[:playermat_lowest_id_idx]
        )
        playermats_player_ids = [playermat.id for playermat in playermats_by_player_id]

        # confirm it incremented the player_order by id's
        self.assertEqual(
            sorted(playermats_player_ids),
            playermats_player_ids,
            "The player order did not " "implement 'clockwise' player order iteration.",
        )

    def test_player_order_turn_one_solo(self):
        game = self.create_one_player_game()
        game.current_turn = GameTurn.initialize_turn(game)
        game.save()

        game.determine_player_order()

        # confirm that first player is NOT joan
        joan_player = JoanAI.get_user_joan()
        player_one = game.playermat_set.filter(player_order=1)[0]
        self.assertNotEqual(player_one, joan_player)

    def test_player_order_turn_six_max_horses(self):
        game = self.create_three_player_game()
        game.current_turn = GameTurn.initialize_turn(game)
        game.save()

        # set initial turn order as 3rd player first
        with mock.patch("random.choice", side_effect=lambda seq: seq[2]):
            game.determine_player_order()

        # setup the 3 playermats with horses, with player_order = 3 as winner
        horses = 1
        playermats = game.playermat_set.all().order_by("player_order")
        for playermat in playermats:
            playermat.horses = horses
            playermat.save()
            horses += 1

        # 3rd player before should become player 1
        third_player = playermats[2]

        # set current_turn to not first turn
        game.current_turn = GameTurn.initialize_turn(game, 6)
        game.save()

        game.determine_player_order()
        first_player = game.playermat_set.all().order_by("player_order")[0]

        # confirm that previous 3rd player (with max horses) is now first
        self.assertEqual(
            third_player.id,
            first_player.id,
            "Player order not " "choosing player with max horses as expected.",
        )

    def test_player_order_turn_six_horses_tied(self):
        game = self.create_three_player_game()
        game.current_turn = GameTurn.initialize_turn(game)
        game.save()

        # set initial turn order as 3rd player first
        with mock.patch("random.choice", side_effect=lambda seq: seq[2]):
            game.determine_player_order()

        # setup the 3 playermats to have tied horses with 2 players
        horses = 4
        playermats = game.playermat_set.all().order_by("player_order")
        # set first two players as 'tied'
        for playermat in playermats[:2]:
            playermat.horses = horses
            playermat.save()

        # 2nd player before will become player 1
        second_player = playermats[1]

        # set current_turn to not first turn
        game.current_turn = GameTurn.initialize_turn(game, 6)
        game.save()

        game.determine_player_order()
        first_player = game.playermat_set.all().order_by("player_order")[0]

        # confirm that previous 3rd player (with max horses) is now first
        self.assertEqual(
            second_player.id,
            first_player.id,
            "Player order not " "choosing player in clockwise when horses tied.",
        )

    def test_setup_choice_dice_for_turn_one_player(self):
        # one playermat, minus Turn 1 choice dice
        dice_bank_counts = {
            ResourceType.WOOD: 12,  # minus the 2 given wood
            ResourceType.STONE: 12,  # minus the 2 given stone
            ResourceType.GOLD: 12,  # minus the 1 given gold
            ResourceType.LAND: 11,
            ResourceType.IRON: 11,
        }
        dice_bank_list = self.create_expected_die_list(dice_bank_counts)
        game = self.create_one_player_game()
        game.current_turn = GameTurn.initialize_turn(game)
        game.save()
        game.setup_choice_dice_for_turn()

        # confirm only playermat in the set has base choice dice
        playermat = game.playermat_set.get()
        self.assertEqual(
            playermat.choice_dice,
            [
                ResourceType.WOOD,
                ResourceType.WOOD,
                ResourceType.STONE,
                ResourceType.STONE,
                ResourceType.GOLD,
            ],
        )
        self.assertEqual(game.dice_bank, dice_bank_list)

    def test_setup_choice_dice_for_turn_two_player(self):
        # minus Turn 2 choice dice * two playermat
        dice_bank_counts = {
            ResourceType.WOOD: 12,  # minus the 1 given wood * 2
            ResourceType.STONE: 12,  # minus the 1 given stone * 2
            ResourceType.GOLD: 9,  # minus the 2 given gold * 2
            ResourceType.LAND: 11,
            ResourceType.IRON: 11,
        }
        dice_bank_list = self.create_expected_die_list(dice_bank_counts)

        game = self.create_two_player_game()
        game.current_turn = GameTurn.initialize_turn(game, 2)
        game.save()
        game.setup_choice_dice_for_turn()

        # confirm all playermats in the set have base choice dice
        for playermat in game.playermat_set.all():
            self.assertCountEqual(
                playermat.choice_dice,
                [
                    ResourceType.WOOD,
                    ResourceType.STONE,
                    ResourceType.GOLD,
                    ResourceType.GOLD,
                ],
            )

        self.assertCountEqual(game.dice_bank, dice_bank_list)

    def test_setup_choice_dice_for_turn_three_player(self):
        # minus Turn 3 choice dice * three playermat
        dice_bank_counts = {
            ResourceType.WOOD: 5,  # minus the 3 given wood * 3
            ResourceType.STONE: 11,  # minus the 1 given stone * 3
            ResourceType.GOLD: 10,  # minus the 1 given gold * 3
            ResourceType.LAND: 11,
            ResourceType.IRON: 11,
        }

        dice_bank_list = self.create_expected_die_list(dice_bank_counts)

        game = self.create_three_player_game()
        game.current_turn = GameTurn.initialize_turn(game, 3)
        game.save()
        game.setup_choice_dice_for_turn()

        # confirm all playermats in the set have base choice dice
        for playermat in game.playermat_set.all():
            self.assertEqual(
                playermat.choice_dice,
                [
                    ResourceType.WOOD,
                    ResourceType.WOOD,
                    ResourceType.WOOD,
                    ResourceType.STONE,
                    ResourceType.GOLD,
                ],
            )

        self.assertEqual(game.dice_bank, dice_bank_list)


class TestGameTurn(BaseGameTest):
    def test_create_game_turn(self):
        game = self.create_two_player_game()
        game_turn = GameTurn(game=game, turn_no=1, first_player=self.user)
        game_turn.save()

        fetched_turn = GameTurn.objects.get(id=game_turn.id)

        self.assertEqual(game_turn, fetched_turn)

    def test_initialize_first_turn(self):
        game = self.create_two_player_game()

        first_game_turn = GameTurn.initialize_turn(game)

        self.assertEqual(first_game_turn.turn_no, 1)
        self.assertEqual(first_game_turn.game, game)

    def test_initialize_other_turn(self):
        game = self.create_two_player_game()

        first_game_turn = GameTurn.initialize_turn(game, 3)

        self.assertEqual(first_game_turn.turn_no, 3)
        self.assertEqual(first_game_turn.game, game)
