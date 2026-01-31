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
    key_str = bytes.fromhex(rfc_key_hex).decode("latin-1")
    nonce_hex = "000000090000004a00000000" 
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

# Test Vector for the ChaCha20 Keystream Generation
# https://datatracker.ietf.org/doc/html/rfc7539#section-2.3.2
def test_keys_from_RFC(matrix):
    keystream = chacha20.chacha20_keystream_chunk(matrix)
    assert keystream.hex() == "10f1e7e4d13b5915500fdd1fa32071c4c7d1f4c733c068030422aa9ac3d46c4ed2826446079faa0914c2d705d98b02a2b5129cd1de164eb9cbd083e8a2503c4e"
    print("Keystream from RFC test passed")

# Test Vector for the ChaCha20 Cipher
# https://datatracker.ietf.org/doc/html/rfc7539#section-2.3.2
def test_chacha20_cipher_from_RFC():
    rfc_key_hex = "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f"
    key_str = bytes.fromhex(rfc_key_hex).decode("latin-1") 
    nonce_hex = "000000000000004a00000000"  
    plaintext_hex = "4c616469657320616e642047656e746c656d656e206f662074686520636c617373206f66202739393a204966204920636f756c64206f6666657220796f75206f6e6c79206f6e652074697020666f7220746865206675747572652c2073756e73637265656e20776f756c642062652069742e"
    plaintext_bytes = bytes.fromhex(plaintext_hex)
    expected_ciphertext_hex = "6e2e359a2568f98041ba0728dd0d6981e97e7aec1d4360c20a27afccfd9fae0bf91b65c5524733ab8f593dabcd62b3571639d624e65152ab8f530c359f0861d807ca0dbf500d6a6156a38e088a22b65e52bc514d16ccf806818ce91ab77937365af90bbf74a35be6b40b8eedf2785e42874d"
    expected_ciphertext_bytes = bytes.fromhex(expected_ciphertext_hex)
    ciphertext = chacha20.chacha20_encrypt(plaintext_bytes, key_str, nonce_hex)
    assert ciphertext == expected_ciphertext_bytes
    decrypted = chacha20.chacha20_decrypt(ciphertext, key_str, nonce_hex)
    assert decrypted == plaintext_bytes
    print("ChaCha20 Cipher test passed")

test_quarter_round()
test_matrix = test_matrix_from_RFC()
test_keys_from_RFC(test_matrix)
test_chacha20_cipher_from_RFC()

