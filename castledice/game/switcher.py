from .solo_ai import JoanActions, JoanAI

PHASE_VIEW_MAPPER = {
    0: "waiting",  # default when in between phases for a player
    1: "player_order",  # Determine Player Order
    2: None,  # Choose cards
    3: "choose_dice",
    4: "roll_dice",
    5: "gather_dice",
    6: None,  # Go to Market
    7: None,  # Workers Produce
    8: None,  # Merchants Work
    9: None,  # Build
    10: None,  # Barbarians Raid
}


class Switcher(object):
    def trigger_wait_for_current_player(self):
        pass

    @classmethod
    def initiate_next_turn(cls, game):
        if game.turn < 7:
            game.advance_turn()
            for playermat in game.playermat_set.all():
                playermat.reset_turn_based()
        else:
            # end game
            pass

    @classmethod
    def initiate_next_phase(cls, game):
        game.advance_phase()

        if game.current_phase > 10:
            cls.initiate_next_turn(game)

    @classmethod
    def is_player_waiting(cls, game, player):
        """

        :param game.models.Game game:
        :param django.contrib.auth.models.User player:
        :return:
        """

        if game.current_player == JoanAI.get_user_joan():
            JoanActions.execute(game)
            game.advance_current_player()

        if game.current_player != player:
            return True

        return False

    @classmethod
    def advance_round_player(cls, game):
        game.advance_current_player()

        if game.current_player == JoanAI.get_user_joan():
            JoanActions.execute(game)
            game.advance_current_player()

        # if not gather phase
        if game.current_phase != 5:
            # this phase is over if back to player 1
            if game.get_current_player_playermat().player_order == 1:
                cls.initiate_next_phase(game)

        # gather phase, ends when out of dice
        elif not game.gather_dice:
            cls.initiate_next_phase(game)

    @classmethod
    def send_player_to_view(cls, game, player):
        if cls.is_player_waiting(game, player):
            return PHASE_VIEW_MAPPER[0]

        if cls.is_unbuilt_phase(game):
            return "pass_phase"

        return PHASE_VIEW_MAPPER[game.current_phase]

    @classmethod
    def is_unbuilt_phase(cls, game):
        return PHASE_VIEW_MAPPER[game.current_phase] is None
