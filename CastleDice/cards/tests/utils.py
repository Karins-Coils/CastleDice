import unittest
from typing import Callable

from CastleDice.common import PhaseType

__all__ = [
    'skip_if_not_implemented',
    'skip_test_if_base_class',
    'CardTestBase',
]


def skip_test_if_base_class(f: Callable) -> Callable:
    """
    Handy decorator that when added to a test, will check if the test is on the base class
    or on the child class. Child classes are expected to have set their card_class and should
    be able to run all tests
    """
    def wrapper(self, *args, **kwargs):
        # check here is primitive.  We assume all children are setting which card they are using
        if self.card_class is not None:
            f(self, *args, **kwargs)
        else:
            # self.skipTest("Skipping on base parent class")
            # silently skip these tests, since they SHOULD pass and be happy on any bases classes
            pass
    return wrapper


def skip_if_not_implemented(func_name: str) -> Callable:
    """
    Helpful decorator in the interim while I get functions routed together.  Does not explicitly
    fail tests that raise a NotImplementedError

    Should ALWAYS be paired with @skip_test_if_base_class within a base class
    """
    def deco(f: Callable) -> Callable:
        def wrapper(self, *args, **kwargs):
            # confirm the function is written and not throwing a NotImplementedError
            try:
                method = getattr(self.card, func_name)
                method()
            except NotImplementedError:
                # leaving this as a skip, since it SHOULD show and be something I fix down the line
                self.skipTest("Method has not been implemented yet, but should be")
            except Exception:
                # catching all other generic exceptions, since we expect it likely to complain
                # without state/args/etc
                f(self, *args, **kwargs)
        return wrapper
    return deco


class CardTestBase(unittest.TestCase):
    card_class = None
    card_type = None
    deck_name = None
    playable_phase_type = None
    ongoing_phase_type = None
    has_description = False
    has_build_cost = False
    victory_points = 0

    def setUp(self):
        self.card = None
        if self.card_class:
            self.card = self.card_class()

    # -- helper functions -- #

    # -- Test card props -- #
    @skip_test_if_base_class
    def test_base_properties(self):
        self.assertTrue(self.card)
        self.assertEqual(self.card.card_id, self.card_type.value)
        self.assertTrue(self.card.name)

    @skip_test_if_base_class
    def test_description(self):
        if self.has_description:
            self.assertIsNotNone(self.card.description)
        else:
            self.assertIsNone(self.card.description)

    @skip_test_if_base_class
    def test_playable_phase(self):
        self.assertEqual(self.card.playable_phase, self.playable_phase_type)

    @skip_test_if_base_class
    def test_ongoing_phase(self):
        self.assertEqual(self.card.ongoing_phase, self.ongoing_phase_type)

    @skip_test_if_base_class
    def test_deck_type(self):
        self.assertEqual(self.card.deck_type, self.deck_name)

    @skip_test_if_base_class
    def test_victory_points(self):
        self.assertEqual(self.card.victory_points, self.victory_points)

    @skip_test_if_base_class
    def test_build_cost(self):
        if self.has_build_cost:
            self.assertTrue(len(self.card.build_cost))
            self.assertEqual(self.card.playable_phase, PhaseType.BUILD)
        else:
            self.assertEqual(self.card.build_cost, ())

    # -- Test card functions -- #
    @skip_test_if_base_class
    @skip_if_not_implemented('is_playable')
    def test_is_playable(self):
        self.fail("Must implement this feature and its test")

    @skip_test_if_base_class
    @skip_if_not_implemented('play')
    def test_play(self):
        self.fail("Must implement this feature and its test")

    @skip_test_if_base_class
    @skip_if_not_implemented('score')
    def test_score(self):
        if self.victory_points > 0:
            self.fail("Must implement this feature and its test")

    @skip_test_if_base_class
    @skip_if_not_implemented('discard')
    def test_discard(self):
        self.fail("Must implement this feature and its test")

    @skip_test_if_base_class
    @skip_if_not_implemented('use_ongoing')
    def test_use_ongoing(self):
        self.fail("Must implement this feature and its test")

    @skip_test_if_base_class
    @skip_if_not_implemented('has_ongoing_choice')
    def test_has_ongoing_choice(self):
        self.fail("Must implement this feature and its test")

    @skip_test_if_base_class
    @skip_if_not_implemented('can_use_ongoing')
    def test_can_use_ongoing(self):
        self.fail("Must implement this feature and its test")

    @skip_test_if_base_class
    @skip_if_not_implemented('reset_ongoing')
    def test_reset_ongoing(self):
        self.fail("Must implement this feature and its test")
