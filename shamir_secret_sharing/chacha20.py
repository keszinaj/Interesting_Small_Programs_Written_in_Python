# made by keszinaj
# chacha20 RFC makes us use 32 bit athematic operations
# I don't know any defoult way to do that in python so I have decided
# to use bit mask to simulate 32 bit operations 
# python...
# we also need to mimic the operation in 32 bit space
# chacha20 is using rotate left(NOT shift left) and adding
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

            
def chacha20(initial_state_matrix):
    matrix = initial_state_matrix.copy()
    for i in range(20):
        if i % 2 == 0:
            chacha20_diagonal_operations(matrix)
        else:
            chacha20_columns_operations(matrix)
    for i in range(4):
        for j in range(4):
            matrix[i][j] = add32(matrix[i][j], initial_state_matrix[i][j])
    flat_state = [matrix[r][c] for r in range(4) for c in range(4)]
    #keystream_block = b''.join(w.to_bytes(4, 'little') for w in flat_state)    
    return keystream_block
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
    if(len(nonce) !=12):
        print("Nonce length error")
        return "Nonce length error"
    nonce_in_parts = [nonce[i:i+4] for i in range(0, len(nonce), 4)]
    nonce_in_blocks=[]
    for p in nonce_in_parts:
        b = p.encode("ascii")
        n = int.from_bytes(b, "little")
        print(hex(n))
        nonce_in_blocks.append(n)
    print("Nonce ", nonce_in_blocks)
    initial_matrix[3][1:] = nonce_in_blocks.copy()    
    #prapare counter
    f_counter = counter.to_bytes(4, byteorder="little")
    f_counter = int.from_bytes(f_counter, "little")
    initial_matrix[3][0] = f_counter
    print("Initial matrix:")
    print(initial_matrix)


create_matrix('12345678912345678912345678912312',"alaiolamakot",1) 