import argparse
import sys
from pathlib import Path

from axolpy.cryptography import (decrypt_message, encrypt_message,
                                 generate_key_file)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--generate-key-file",
                        action="store_true",
                        required=False,
                        help="Generate a key file. If this is specified, other arguments are ignored.")
    parser.add_argument("-k", "--key-file",
                        required=False,
                        help="The path to the key file.")
    parser.add_argument("-e", "--encrypt",
                        action="store_true",
                        required=False,
                        help="Encrypt a message.")
    parser.add_argument("-d", "--decrypt",
                        action="store_true",
                        required=False,
                        help="Decrypt a message.")
    parser.add_argument("-m", "--message",
                        required=False,
                        help="Message to encrypt or decrypt. If not specified, read from stdin.")
    if len(sys.argv) == 1:
        parser.print_help()
        return
    args = parser.parse_args()

    if args.generate_key_file:
        generate_key_file()
        return

    if not args.key_file:
        print("Key file not specified.")
        return 1

    if not args.encrypt and not args.decrypt:
        print("--encrypt or --decrypt must be specified.")
        return 1

    if not args.message:
        print("Message not specified.")
        return 1

    if args.encrypt:
        message = encrypt_message(
            message=args.message, key=Path(args.key_file))
        print(message.decode())
    elif args.decrypt:
        message = decrypt_message(
            encrypted_message=args.message, key=Path(args.key_file))
        print(message.decode())


if __name__ == "__main__":
    sys.exit(main())
