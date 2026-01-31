# made by keszinaj
# This file contains test cases from RFC vectors for ChaCha20 encryption/decryption algorithm.
# Note that implementation not directly fallows every RFC specification, some function structures is not the same
# However at the end the output should be the same as in the RFC standard becouse the logic of the algorithm is implemented correctly.
# Testing vectors are taken from: https://datatracker.ietf.org/doc/html/rfc7539

import chacha20


# Test Vector for the ChaCha Quarter Round
# https://datatracker.ietf.org/doc/html/rfc7539#section-2.1.1
def test_quarter_round():
    a = 0x11111111
    b = 0x01020304
    c = 0x9b8d6f43
    d = 0x01234567
    a, b, c, d = chacha20.chacha20_one_operation_abcd(a,b,c,d)
    assert a == 0xea2a92f4
    assert b == 0xcb1cf8ce
    assert c == 0x4581472e
    assert d == 0x5881c4bb
    print("Quarter Round test passed")

# Test Vector for the ChaCha20 Block Function
# https://datatracker.ietf.org/doc/html/rfc7539#section-2.3.2
def test_matrix_from_RFC():
    rfc_key_hex = "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f"
    key_str = bytes.fromhex(rfc_key_hex).decode("latin-1")  # preserves raw byte values
    nonce_hex = "000000090000004a00000000"  # example 12-byte nonce as 24 hex chars
    matrix = chacha20.create_matrix(key_str, nonce_hex, counter=1)
    expected_matrix = [
        [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574],
        [0x03020100, 0x07060504, 0x0b0a0908, 0x0f0e0d0c],
        [0x13121110, 0x17161514, 0x1b1a1918, 0x1f1e1d1c],
        [0x00000001, 0x09000000, 0x4a000000, 0x00000000]
    ]
    assert matrix == expected_matrix
    print("Matrix from RFC test passed")
    return matrix




test_quarter_round()
test_matrix_from_RFC()

