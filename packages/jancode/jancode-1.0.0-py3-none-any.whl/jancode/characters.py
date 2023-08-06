def combination(number: str) -> str:
    """
    Return a combination of odd and even parity
    """
    combi = [
        "OOOOOO",
        "OOEOEE",
        "OOEEOE",
        "OOEEEO",
        "OEOOEE",
        "OEEOOE",
        "OEEEOO",
        "OEOEOE",
        "OEOEEO",
        "OEEOEO",
    ]

    return combi[int(number)]


def left_odd_characters(number: str) -> str:
    characters = [
        "0001101",
        "0011001",
        "0010011",
        "0111101",
        "0100011",
        "0110001",
        "0101111",
        "0111011",
        "0110111",
        "0001011",
    ]

    return characters[int(number)]


def left_even_characters(number: str) -> str:
    characters = [
        "0100111",
        "0110011",
        "0011011",
        "0100001",
        "0011101",
        "0111001",
        "0000101",
        "0010001",
        "0001001",
        "0010111",
    ]

    return characters[int(number)]


def right_even_characters(number: str) -> str:
    characters = [
        "1110010",
        "1100110",
        "1101100",
        "1000010",
        "1011100",
        "1001110",
        "1010000",
        "1000100",
        "1001000",
        "1110100",
    ]

    return characters[int(number)]
