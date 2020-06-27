from decimal import Decimal
import sys
import os


def get_current_directory():
    if getattr(sys, "frozen", False):
        # Frozen means the program is running as an exe
        return os.path.dirname(sys.executable)

    return os.path.dirname(__file__)


def normalize(number):
    """
    Removes all trailing 0s, if there are any.
    Returns a Decimal object of given number.
    """

    number = str(number)
    idx = 0
    if "." in number:
        for dec in reversed(number):
            if dec == "0":
                number = number[:-1]
            else:
                break

    return Decimal(number)

