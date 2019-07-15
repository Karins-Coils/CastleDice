from typing import Callable

__all__ = [
    'create_skip_if_not_implemented_decorator',
    'create_skip_test_if_base_class_decorator',
]


def create_skip_test_if_base_class_decorator(child_attr: str) -> Callable:
    """A function that creates a custom decorator for use on a Base Test class, to allow the base
    test class not show failed or skipped tests, when they aren't real tests but templates for
    child test classes

    Example usage:

    skip_test_if_base_class = create_skip_test_if_base_class_decorator('card_class')

    class SomeBaseTest(unittest.TestCase):
        card_class = None  # required on child classes

        @skip_test_if_base_class
        def test_success(self):
            pass

    :param child_attr: an attribute that will be None on the parent, but will be set on children
    :type: str
    :return: a decorator to be used on any test method
    :rtype: Callable
    """
    def decorator(f: Callable) -> Callable:
        """
        Handy decorator that when added to a test, will check if the test is on the base class
        or on the child class. Child classes are expected to have set their child_attr and should
        be able to run all tests
        """
        def wrapper(self, *args, **kwargs):
            # check here is primitive.
            # We assume all children are setting this child_attr
            if getattr(self, child_attr) is not None:
                f(self, *args, **kwargs)
            else:
                # self.skipTest("Skipping on base parent class")
                # silently skip these tests, since they SHOULD pass
                # and be happy on any bases classes
                pass
        return wrapper
    return decorator


def create_skip_if_not_implemented_decorator(obj_with_function: str) -> Callable:
    """A function that creates a custom decorator for use on test functions, to allow the test
    method to skip if the related method has not been fully implemented (i.e. is throwing
    NotImplementedError).  When using on a base class, should be paired with
    @skip_test_if_base_class

    Example usage:

    skip_if_not_implemented = create_skip_if_not_implemented_decorator('card')

    class SomeBaseTest(unittest.TestCase):
        card = None  # object on child classes

        @skip_test_if_base_class
        @skip_if_not_implemented('play')  # 'play' expected on the 'card' object
        def test_success(self):
            pass

    :param obj_with_function: the object on the test class, that should have the below function set
    :type: str
    :return:
    """
    def outer_deco(func_name: str) -> Callable:
        """
        Helpful decorator in the interim while I get functions routed together.
        Does not explicitly fail tests that raise a NotImplementedError

        Should ALWAYS be paired with @skip_test_if_base_class within a base class
        """
        def inner_deco(f: Callable) -> Callable:
            def wrapper(self, *args, **kwargs):
                obj = getattr(self, obj_with_function)
                # confirm the function is written and not throwing a NotImplementedError
                try:
                    method = getattr(obj, func_name)
                    method()
                except NotImplementedError:
                    # leaving this as a skip, since it SHOULD show and be
                    # something I fix down the line
                    self.skipTest("Method has not been implemented yet, but should be")
                except Exception:
                    # catching all other generic exceptions, since we expect it likely to complain
                    # without state/args/etc
                    f(self, *args, **kwargs)
            return wrapper
        return inner_deco
    return outer_deco
