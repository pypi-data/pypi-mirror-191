import jancode.characters as characters


def binary(jancode: str, combination: str, center: int) -> str:
    """
    Converts input numbers to binary numbers for JAN code and adds guard bars
    """
    binary_number: str = ""
    left_right_guard: str = "101"
    center_guard: str = "01010"

    # The left guard bar added
    binary_number += left_right_guard

    for i in range(len(jancode)):
        if i < center:
            binary_number = convert_left(i, jancode, combination, binary_number)
        elif i == center:
            binary_number = convert_left(i, jancode, combination, binary_number)
            binary_number += center_guard
        elif i > center:
            binary_number += characters.right_even_characters(jancode[i])

    # The right guard bar added
    binary_number += left_right_guard

    return binary_number


def convert_left(i: int, jancode: str, combination: str, binary_number: str) -> None:
    if combination[i] == "O":
        binary_number += characters.left_odd_characters(int(jancode[i]))
    else:
        binary_number += characters.left_even_characters(int(jancode[i]))

    return binary_number
