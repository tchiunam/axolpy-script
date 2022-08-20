import argparse
import sys
import textwrap

from axolpy.cryptography import (decrypt_message, encrypt_message,
                                 generate_key_file, load_key)
from axolpy.util import prompt as axolpy_prompt
from prompt_toolkit import prompt


def main() -> int:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            Encrypt or decrypt a message. The output is written to stdout.

            By default, encryption is executed. To decrypt, use the --decrypt.
            '''))
    parser.add_argument("-g", "--generate-key-file",
                        action="store_true",
                        required=False,
                        help="Generate a key file. If this is specified, other arguments are ignored.")
    parser.add_argument("-k", "--key-file",
                        required=False,
                        help="The path to the key file.")
    parser.add_argument("-d", "--decrypt",
                        action="store_true",
                        required=False,
                        help="Decrypt a message.")
    parser.add_argument("-m", "--message",
                        required=False,
                        help="Message to encrypt or decrypt. If not specified, read from stdin.")
    args = parser.parse_args()

    if args.generate_key_file:
        generate_key_file()
        return

    key: bytes = None
    if args.key_file:
        key = load_key(args.key_file)
    else:
        key_input = prompt(
            message="Key: ",
            validator=axolpy_prompt.CryptographyKeyValidator())
        key = key_input.encode()

    message = args.message
    if not message:
        print("Start typing the message to be encrypted or decrypted. Press Escape+Enter to submit.")
        message = prompt(multiline=True)

    if args.decrypt:
        message = decrypt_message(
            encrypted_message=message,
            key=key)
        print(message.decode())
    else:
        message = encrypt_message(
            message=message,
            key=key)
        print(message.decode())


if __name__ == "__main__":
    sys.exit(main())
