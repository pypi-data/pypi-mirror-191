import sys
import os

import jancode.check_digit as checkdigit
import jancode.convert as convert
import jancode.property as property
import jancode.create_svg as svg


def check_digit(number: str, length: int) -> None:
    """
    Calculate the check digit
    """
    if checkdigit.check(number, length):
        print("Check digit is correct.")
    else:
        print("Check digit is incorrect.")
        sys.exit()


def generate(number: int | str, path: str = ".") -> None:
    """
    Generate JAN code
    """
    length, jancode_number, center_position, combi, jancode_type = property.set_property(
        str(number)
    )
    check_digit(str(number), length)
    binary_number: str = convert.binary(jancode_number, combi, center_position)

    os.makedirs(path, exist_ok=True)
    svg.create(binary_number, len(binary_number), path, str(number), jancode_type)
