def calculation(number, length) -> int:
    """
    Calculation Method
    1. Add even-digit numbers and multiply by 3.
    2. Add odd-numbered digits (excluding the last digit, which is the check digit).
    3. Add even-digit and odd-digit numbers and look at the 1's in the value.
    4. Subtract a number to the first place from 10 (If the number obtained in 3 is 0, the check digit is 0).
    """

    even_number = (sum(int(number[i]) for i in range(1, length, 2))) * 3
    odd_number = sum(int(number[i]) for i in range(0, length - 1, 2))
    ones_place: int = (even_number + odd_number) % 10
    calculated_checkdigit = 0 if ones_place == 0 else 10 - ones_place

    return calculated_checkdigit


def check(number: str, length: int) -> bool:
    """
    Check if the entered checkdigit matches the calculated checkdigit
    """
    input_checkdigit: int = int(number[length - 1])
    if input_checkdigit == calculation(number, length):
        return True
    else:
        return False
