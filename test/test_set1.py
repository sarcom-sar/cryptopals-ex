import pytest
from crypals import set1


def test_hex_to_base64():
    assert set1.hex_to_base64("") == ""
    assert set1.hex_to_base64("ffffff") == "////"
    assert set1.hex_to_base64("0a0a") == "Cgo="
    assert set1.hex_to_base64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d") == "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

    with pytest.raises(AssertionError) as exinfo:
        set1.hex_to_base64("0ca")
    assert str(exinfo.value) == "Doesn't contain multiple of 1 byte"

    with pytest.raises(ValueError) as exinfo:
        set1.hex_to_base64("trfg")
    assert str(exinfo.value) == "invalid literal for int() with base 16: 't'"


def test_xor_pair():
    assert set1.xor_pair("00", "00") == "00"
    assert set1.xor_pair("110", "010") == "100"
    assert set1.xor_pair("abc", "fed") == "551"
    assert set1.xor_pair("1c0111001f010100061a024b53535009181c",
                         "686974207468652062756c6c277320657965") ==\
           "746865206b696420646f6e277420706c6179"

    with pytest.raises(AssertionError) as exinfo:
        set1.xor_pair("01d", "9d")
    assert str(exinfo.value) == "Strings are not equal size"


def test__try_xor_val():
    assert set1._try_xor_val("4d", 0x1) == [0x4c]
    assert set1._try_xor_val("", 0x1) == []
    assert set1._try_xor_val("32", 0x1) == [0x33]
    assert set1._try_xor_val("48656C6C6F20576F726C64", 0) == [72, 101, 108, 108, 111, 32, 87, 111, 114, 108, 100]


def test__score_xors():
    assert set1._score_xors("eee") == 33
    assert set1._score_xors("ggg") == 6
    assert set1._score_xors("aing") == 23
    assert set1._score_xors("") == 0


def test_find_xor_cipher_solution():
    assert set1.find_xor_cipher_solution("1b37373331363f78151b7f2b783431333d783"
                                         "97828372d363c78373e783a393b3736") ==\
           ("Cooking MC's like a pound of bacon", 124)

    assert set1.find_xor_cipher_solution("48656C6C6F20576F726C64") ==\
           ("Hello World", 50)


def test_find_single_xor_in_huge_list():
    assert set1.find_single_xor_in_huge_list() ==\
        ('Now that the party is jumping\n', 112)
