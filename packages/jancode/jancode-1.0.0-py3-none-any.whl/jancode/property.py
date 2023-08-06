from jancode.characters import combination


def set_property(number: str) -> None:
    """
    Set the length and height of the JAN code
    """
    guard_bar_length: int = 11  # Guard bar length
    length: int = len(number)

    if length == 13:
        # Subtract the first digit of the standard barcode because the standard barcode has 12 digits.
        jancode_number: str = number[1:]
        center: int = 5
        combi = combination(number[0])
        jancode_type = "standard"
    else:
        center = 3
        jancode_number = number
        combi: str = (
            "OOOO"  # For short type, all strings on the left side are odd parity.
        )
        jancode_type = "short"

    return length, jancode_number, center, combi, jancode_type
