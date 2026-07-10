LETTER_CODE_MAP: dict[str, int] = {
    "A": 10,
    "B": 11,
    "C": 12,
    "D": 13,
    "E": 14,
    "F": 15,
    "G": 16,
    "H": 17,
    "I": 34,
    "J": 18,
    "K": 19,
    "L": 20,
    "M": 21,
    "N": 22,
    "O": 35,
    "P": 23,
    "Q": 24,
    "R": 25,
    "S": 26,
    "T": 27,
    "U": 28,
    "V": 29,
    "W": 32,
    "X": 30,
    "Y": 31,
    "Z": 33,
}


def is_valid_taiwan_id(user_id: str) -> bool:
    if len(user_id) != 10:
        return False

    if not user_id[0].isalpha() or not user_id[1:].isdigit():
        return False

    first_char: str = user_id[0].upper()
    if first_char not in LETTER_CODE_MAP:
        return False

    transformed_code: int = LETTER_CODE_MAP[first_char]
    digits: list[int] = [int(char) for char in user_id[1:]]

    checksum: int = (transformed_code // 10) + (transformed_code % 10) * 9
    for index, number in enumerate(digits[:-1], start=1):
        checksum += number * (9 - index)
    checksum += digits[-1]

    return checksum % 10 == 0
