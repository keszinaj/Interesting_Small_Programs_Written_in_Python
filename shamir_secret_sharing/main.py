import argparse
import os

def encrypt(args):
    print("Encrypting...")
    

def decrypt(args):
    print("Decrypting...")
    print("File to decrypt: {args.file}")
    keys = []
    n=10
    i=1
    while i<n:
        key = input(f"Enter key #{i}: ")
        if i == 1:
            n_str = key.split("$")[0]
            n = int(n_str) + 2
        keys.append(key)
        i+=1
    print(f"Using keys: {keys}")


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
    decrypt_parser.set_defaults(func=decrypt)

    args = parser.parse_args()
    args.func(args)
    


