# made by keszinaj
# chacha20 RFC makes us use 32 bit athematic operations
# I don't know any defoult way to do that in python so I have decided
# to use bit mask to simulate 32 bit operations 
# python...
# we also need to mimic the operation in 32 bit space
# chacha20 is using rotate left(NOT shift left) and adding
from importlib.resources import path
import os

MASK32 = 0xffffffff
def add32(a, b):
    return (a + b) & MASK32
def rotl32(a, n):
    return ((a << n) | (a >> (32 - n))) & MASK32

def chacha20_one_operation_abcd(a,b,c,d):
    a = add32(a, b); d ^= a; d = rotl32(d, 16)
    c = add32(c, d); b ^= c; b = rotl32(b, 12)
    a = add32(a, b); d ^= a; d = rotl32(d,  8)
    c = add32(c, d); b ^= c; b = rotl32(b,  7)
    return a, b, c, d
#test vector
'''
a = 0x11111111
b = 0x01020304
c = 0x9b8d6f43
d = 0x01234567
for x in chacha20_one_operation_abcd(a,b,c,d):
    print(hex(x))
print("----")
'''

#it should return:
#a = 0xea2a92f4
#b = 0xcb1cf8ce
#c = 0x4581472e
#d = 0x5881c4bb
# test is passing


# In chacha20 there are 20 rounds,
# on odd rounds we do operations on columns
# on even rounds we do operations on diagonals
def chacha20_columns_operations(matrix):
    for i in range(4):
        a = matrix[0][i]
        b = matrix[1][i]
        c = matrix[2][i]
        d = matrix[3][i]
        a, b, c, d = chacha20_one_operation_abcd(a, b, c, d)
        matrix[0][i] = a
        matrix[1][i] = b
        matrix[2][i] = c
        matrix[3][i] = d

def chacha20_diagonal_operations(matrix):
    for i in range(4):
        a = matrix[0][(0+i)%4]
        b = matrix[1][(1+i)%4]
        c = matrix[2][(2+i)%4]
        d = matrix[3][(3+i)%4]
        a, b, c, d = chacha20_one_operation_abcd(a, b, c, d)
        matrix[0][(0+i)%4] = a
        matrix[1][(1+i)%4] = b
        matrix[2][(2+i)%4] = c
        matrix[3][(3+i)%4] = d
        
def chacha20_keystream_chunk(initial_state_matrix):
    #jak mnie python zrobil
    #matrix = initial_state_matrix.copy()
    matrix = [row[:] for row in initial_state_matrix]
    for row in initial_state_matrix:
        for word in row:
            print(hex(word), end=' ')
        print("KONIEC")
    for i in range(1,21):
        if i % 2 == 0:
            chacha20_diagonal_operations(matrix)
        else:
            chacha20_columns_operations(matrix)
    for row in matrix:
        for word in row:
            print(hex(word), end=' ')
        print() 
    for i in range(4):
        for j in range(4):
            matrix[i][j] = add32(matrix[i][j], initial_state_matrix[i][j])
    for row in matrix:
        for word in row:
            print(hex(word), end=' ')
        print()
    keystream = b"".join( word.to_bytes(4, "little")
                         for row in matrix
                         for word in row)
    print("Keystream block:")
    print(keystream.hex())
    print(len(keystream))
      
    return keystream
'''
key has to be 32 bytes long == 32 letters, it has to be in string format
nonce has to be 12 bytes long == 12 letters, it has to be in string format
counter is integer
'''
def create_matrix(key,nonce,counter):
    initial_matrix = [[0 for _ in range(4)] for _ in range(4)]
    # const is sentence "expand 32-byte k" in little endian
    constants = [ 0x61707865, 0x3320646e, 0x79622d32, 0x6b206574 ]
    print(constants)
    initial_matrix[0] = constants.copy()
    # prapere key words
    if(len(key) !=32):
        print("Key length error")
        return "Key length error"
    key_in_parts = [key[i:i+4] for i in range(0, len(key), 4)]
    key_in_blocks=[]
    for k in key_in_parts:
        b = k.encode("ascii")
        n = int.from_bytes(b, "little")
        print(hex(n))
        key_in_blocks.append(n)
    print(key_in_blocks)
    initial_matrix[1] = key_in_blocks[0:4].copy()
    initial_matrix[2] = key_in_blocks[4:8].copy()
    #prepare nonce
    if(len(nonce) !=24): #24 because saved as hex 1 bytes = 2 hex letters
        print("Nonce length error")
        return "Nonce length error"
    nonce = bytes.fromhex(nonce)
    nonce_in_parts = [nonce[i:i+4] for i in range(0, len(nonce), 4)]
    nonce_in_blocks=[]
    for p in nonce_in_parts:
        n = int.from_bytes(p, "little")
        print(hex(n))
        nonce_in_blocks.append(n)
    print("Nonce ", nonce_in_blocks)
    initial_matrix[3][1:] = nonce_in_blocks.copy()    
    #prapare counter
    f_counter = counter.to_bytes(4, byteorder="little")
    f_counter = int.from_bytes(f_counter, "little")
    initial_matrix[3][0] = f_counter
    print(hex(f_counter))
    print("Initial matrix:")
    print(initial_matrix)
    return initial_matrix
# create random nonce and present it in hex format
def create_random_nonce():
    return os.urandom(12).hex()

def test_matrix_from_RFC():
    initial_matrix = [[0 for _ in range(4)] for _ in range(4)]
    key_bytes = bytes.fromhex('000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f')
    key_words = [
        int.from_bytes(key_bytes[i:i+4], "little")
        for i in range(0, 32, 4)
    ]
    constants = [ 0x61707865, 0x3320646e, 0x79622d32, 0x6b206574 ]
    print(constants)
    nonce = bytes.fromhex('000000090000004a00000000')
    nonce_in_blocks = [
        int.from_bytes(nonce[i:i+4], "little")
        for i in range(0, len(nonce), 4)
    ]
    initial_matrix[0] = constants.copy()
    initial_matrix[1] = key_words[0:4].copy()
    initial_matrix[2] = key_words[4:8].copy()
    initial_matrix[3][1:] = nonce_in_blocks.copy() 
    counter = 1 
    f_counter = counter.to_bytes(4, byteorder="little")
    f_counter = int.from_bytes(f_counter, "little")
    initial_matrix[3][0] = f_counter
    print("Initial matrix:", initial_matrix)
    for row in initial_matrix:
        for word in row:
            print(hex(word), end=' ')
        print()
    return initial_matrix
    #for i in key_words:
    #    print(hex(i))

mmm = test_matrix_from_RFC()
chacha20_keystream_chunk(mmm)
'''dobrze wychodzi
   ChaCha state after 20 rounds

       837778ab  e238d763  a67ae21e  5950bb2f
       c4f2d0c7  fc62bb2f  8fa018fc  3f5ec7b7
       335271c2  f29489f3  eabda8fc  82e46ebd
       d19c12b4  b04e16de  9e83d0cb  4e3c50a2

          ChaCha state at the end of the ChaCha20 operation

       e4e7f110  15593bd1  1fdd0f50  c47120a3
       c7f4d1c7  0368c033  9aaa2204  4e6cd4c3
       466482d2  09aa9f07  05d7c214  a2028bd9
       d19c12b5  b94e16de  e883d0cb  4e3c50a2

'''




def chacha20_encrypt(plaintext_bytes, key, nonce):
    data_length = len(plaintext_bytes)
    print()
    chunk_size = 64
    num_of_chunks = (data_length + 63) // 64 
    chunks = [ plaintext_bytes[i:i+chunk_size] for i in range(0, num_of_chunks*chunk_size, chunk_size)]
    cipertext = b""
    for i in range(num_of_chunks):
        keystream = chacha20_keystream_chunk(create_matrix(key, nonce, i+1))
        cipertext_chunk = bytes(b ^ k for b, k in zip(chunks[i], keystream)) # we can't xor on bytes, it will create pair of bytes and xor on it(xor on two numbers)
        cipertext += cipertext_chunk
    return cipertext

def chacha20_decrypt(cipertext_bytes, key, nonce):
    return chacha20_encrypt(cipertext_bytes, key, nonce) # symmetric cipher


with open("./test.txt", "rb") as f:
    plaintext_bytes = f.read()
    nnonnce = create_random_nonce()
    cipertext = chacha20_encrypt(plaintext_bytes, '12345678912345678912345678912312',nnonnce)
    with open("./test.enc", "wb") as f:
      f.write(cipertext)
    decrypted = chacha20_decrypt(cipertext, '12345678912345678912345678912312',nnonnce)
    print(decrypted)