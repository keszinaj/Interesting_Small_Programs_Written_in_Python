import argparse
import shamir_secret_sharing
import chacha20
import hashlib

def encrypt(args):
    print("Encrypting...")
    print(f"File to encrypt: {args.file}")
    print(f"Number of shares to generate: {args.shares}")
    print(f"Threshold number of shares needed to recreate the secret: {args.threshold}")
    nonce = chacha20.create_random_nonce()
    k = args.threshold # number of shares needed to recreate the secret
    n = args.shares    # number of shares to generate
    a = shamir_secret_sharing.random_polynomial(k-1)
    secret_key = "".join(str(i) for i in a)
    #to meke it 32 bytes as chacha20 require
    res = hashlib.md5(secret_key.encode())
    secret_key=res.hexdigest()
    xxx = []
    yyy = []
    for _ in range(n):
        point = shamir_secret_sharing.calculate_random_point_in_polynomial(a, k-1)
        xxx.append(point[0])
        yyy.append(point[1])
        print("Point:", point)
    shared_keys = []
    for i in range(n):
        shared_key = f"c20s${k}${nonce}${xxx[i]}${yyy[i]}"
        shared_keys.append(shared_key)
    print("Shared keys:")
    for sk in shared_keys:
        print(sk)
    print(a)

def decrypt(args):
    print("Decrypting...")
    print("File to decrypt: {args.file}")
    print("Provided secret keys: {args.secretkeys}")
    keys = []
    n=int(args.secretkeys)
    k = 0 # number of shares needed to recreate the secret
    i=1
    xxx=[]
    yyy=[]
    nonce=""
    for i in range(n):
        key = input(f"Enter key #{i}: ")
        if i == 0:
            k = key.split("$")[1]
            nonce = key.split("$")[2]
        xxx.append(int(key.split("$")[3]))
        yyy.append(int(key.split("$")[4]))
    print(xxx)
    print(yyy)
    ta = shamir_secret_sharing.lagrange_polynomial(xxx, yyy)
    print(shamir_secret_sharing.determining_an(ta, xxx))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chacha20 File Encryptor/Decryptor with Samir Secret Sharing Support")
    subparsers = parser.add_subparsers(
    dest="mode",
    required=True,
    help="Select mode. Expected value: encrypt|decrypt"
    )

    encrypt_parser = subparsers.add_parser(
    "encrypt",
    help="Data encryption mode"
    )
    decrypt_parser = subparsers.add_parser(
    "decrypt",
    help="Data decryption mode"
    )

    encrypt_parser.add_argument(
        "--shares",
        type=int,
        required=True,
        help="Number of shares the program will generate"
    )
    encrypt_parser.add_argument(
        "--threshold",
        type=int,
        required=True,
        help="Number of shares that are needed to recreate the secret"
    )
    encrypt_parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to the file that you want to encrypt"
    )
    encrypt_parser.set_defaults(func=encrypt)

    decrypt_parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to the file that you want to decrypt"
    )
    decrypt_parser.add_argument(
        "--secretkeys",
        type=str,
        required=True,
        help="Number of secrets you want to provide for decryption"
    )
    decrypt_parser.set_defaults(func=decrypt)

    args = parser.parse_args()
    args.func(args)
    


