from functools import reduce


def hex_to_base64(hexdata: str) -> str:
    '''
    Takes multiple of 8bit hex data and returns corresponding base64 endoding
    Will throw assertion error if hexdata is not multiple of 8 bits
    '''
    base64_table: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw"\
                        "xyz0123456789+/"
    base64_vals: list[int] = []
    base64_data: str = ""
    padding: int = 0

    # check if hexdata contains only 1byte hexes
    assert (len(hexdata) % 2) == 0, "Doesn't contain multiple of 1 byte"

    dec_vals: list[int] = [int(hexnum, 16) for hexnum in hexdata]

    # combine two 4 bit values into 8 bit number
    dec_vals = [reduce(lambda high_bit, low_bit: (high_bit << 4) + low_bit,
                       bit_pairs) for bit_pairs in zip(dec_vals[::2],
                                                       dec_vals[1::2])]

    while len(dec_vals) % 3 != 0:
        dec_vals.append(0)
        padding += 1

    triplets_24bit: list[int] = [triplets for triplets in
                                 zip(dec_vals[::3],
                                     dec_vals[1::3],
                                     dec_vals[2::3])]

    values_24bit: list[int] = []
    for triplet in triplets_24bit:
        values_24bit.append((triplet[0] << 16) +
                            (triplet[1] << 8) +
                            triplet[2])

    for one_24bit in values_24bit:
        base64_vals.append(one_24bit >> 18 & 0x3F)
        base64_vals.append(one_24bit >> 12 & 0x3F)
        base64_vals.append(one_24bit >> 6 & 0x3F)
        base64_vals.append(one_24bit & 0x3F)

    base64_vals = base64_vals[:-padding] if padding != 0 else base64_vals
    for val in base64_vals:
        base64_data += base64_table[val]

    base64_data += "="*padding

    return base64_data


def xor_pair(first_hex: str, second_hex: str) -> str:
    '''
    Takes hex pair of equal size.
    Returns XORed string
    '''
    assert len(first_hex) == len(second_hex), "Strings are not equal size"

    xored = [int(x, 16) ^ int(y, 16) for x, y in zip(first_hex, second_hex)]

    return ''.join([f'{x:0x}' for x in xored])


def _try_xor_val(tested: str, xor_val: int) -> list[int]:
    return [(int(x+y, 16) ^ xor_val)
            for x, y in zip(tested[::2], tested[1::2])]

def _score_xors(output_string: str) -> int:
    score_table: dict[str, int] = {"e": 11, "m": 3, "a": 8, "h": 3, "r": 7,
                                   "g": 2, "i": 7, "b": 2, "o": 7, "f": 1,
                                   "t": 6, "y": 1, "n": 6, "w": 1, "s": 5,
                                   "k": 1, "l": 5, "v": 1, "c": 4, "u": 3,
                                   "d": 3, "p": 3}

    score: int = sum([score_table[x.lower()] if x in score_table else 0
                      for x in output_string])
    return score


def find_xor_cipher_solution(ciphered_hex: str) -> tuple[int, str]:
    '''
    Based on ciphered_hex which is XORed against single byte
    Returns best scoring solution
    '''
    score_dict: dict[int, str] = {}

    for x in range(256):
        result: str = ''.join([chr(y) for y in _try_xor_val(ciphered_hex, x)])
        score: int = _score_xors(result)
        score_dict[score] = result

    return (score_dict[max(score_dict)], max(score_dict))


def find_single_xor_in_huge_list() -> list[tuple[int, str]]:
    interesting_lines: list[tuple[int, str]] = []
    with open("data/4.txt", "r") as f:
        all_lines: list[str] = f.readlines()

        for line in all_lines:
            interesting_lines.append(find_xor_cipher_solution(line))

    return sorted(interesting_lines, key=lambda x: x[1] > 100, reverse=True)[0]
