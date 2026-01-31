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
    #for row in initial_state_matrix:
    #    for word in row:
    #        print(hex(word), end=' ')
    #    print("KONIEC")
    for i in range(1,21):
        if i % 2 == 0:
            chacha20_diagonal_operations(matrix)
        else:
            chacha20_columns_operations(matrix)
    #for row in matrix:
     #   for word in row:
      #      print(hex(word), end=' ')
       # print() 
    for i in range(4):
        for j in range(4):
            matrix[i][j] = add32(matrix[i][j], initial_state_matrix[i][j])
    #for row in matrix:
    #    for word in row:
    #        print(hex(word), end=' ')
    #    print()
    keystream = b"".join( word.to_bytes(4, "little")
                         for row in matrix
                         for word in row)
    #print("Keystream block:")
    #print(keystream.hex())
    #print(len(keystream))
      
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
    #print(constants)
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
        #print(hex(n))
        key_in_blocks.append(n)
    #print(key_in_blocks)
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
        #print(hex(n))
        nonce_in_blocks.append(n)
    #print("Nonce ", nonce_in_blocks)
    initial_matrix[3][1:] = nonce_in_blocks.copy()    
    #prapare counter
    f_counter = counter.to_bytes(4, byteorder="little")
    f_counter = int.from_bytes(f_counter, "little")
    initial_matrix[3][0] = f_counter
    #print(hex(f_counter))
    #print("Initial matrix:")
   # print(initial_matrix)
    return initial_matrix
# create random nonce and present it in hex format
def create_random_nonce():
    return os.urandom(12).hex()






def chacha20_encrypt(plaintext_bytes, key, nonce):
    data_length = len(plaintext_bytes)
    #print()
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

