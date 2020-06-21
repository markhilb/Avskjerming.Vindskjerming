from decimal import Decimal


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

