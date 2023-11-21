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
    assert (len(hexdata) % 2) == 0

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
        values_24bit.append((triplet[0] << 16) + (triplet[1] << 8) + triplet[2])

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
