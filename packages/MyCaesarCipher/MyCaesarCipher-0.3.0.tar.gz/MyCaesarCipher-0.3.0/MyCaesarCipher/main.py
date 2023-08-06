#!/usr/bin/env python3

from random import randint
from typing import Optional


class CaesarCipher:
    """Cryptographic encryption/decryption techniques using the Caesar-Cipher algorithm.

    ---

    - Substitutes each letter of a message with new "matching" letter shifted down alphabetically by a given amount.

    - Not intended for real-world cryptographic applications, as the Caesar-Cipher algorithm is notoriously easy to crack.

    - More information on this cipher:
        - https://en.wikipedia.org/wiki/Caesar_cipher
    """

    @staticmethod
    def encrypt(text: str,
                key: Optional[int] = None,
                stdout_output: bool = True) -> str:
        """Encrypt text using the Caesar-Cypher cryptography algorithm.

        - Generates encrypted form of :param:`text` using the Caesar-Cipher algorithm.
        - If no :param:`key` is provided, a random integer value is generated.
        - Optionally disable output of encrypted text results to stdout by toggling :param:`stdout_output` to `False`.

        ---

        :param text: text to encrypt.
        :type text: :class:`str`
        :param key: numeric value used to encrypt the given text, defaults to `None`
        :type key: :class:`Optional`[:class:`int`], optional
        :param stdout_output: toggle output to stdout, defaults to `True`
        :type stdout_output: :class:`bool`, optional
        :return: encrypted form of :param:`text`
        :rtype: :class:`str`
        """

        output: str = ''

        #$ Create random key if none provided.
        if key is None:
            key = randint(1, 25)

        #@ Iterate through text char by char.
        for char in text:

            #@ Encrypt uppercase characters
            if (char.isupper()):
                output += chr((ord(char) + key - 65) % 26 + 65)

            #@ Encrypt lowercase characters
            elif (char.islower()):
                output += chr((ord(char) + key - 97) % 26 + 97)

            #@ Encrypt numbers
            elif (char.isdigit()):
                output += str((int(char) + key) % 10)

            #@ Leave all non-alphanumeric characters unchanged.
            else:
                output += char

        info: str = f'> Original Msg : {text}\n\n> Shift-key : {key}\n\n> Encrypted Result: {output}\n'

        if stdout_output:
            print(info)

        return output

    @staticmethod
    def decrypt(text: str, stdout_output: bool = True) -> dict[str, int]:
        """Decrypt Caesar-Cipher encrypted messages and return dictionary of all possible results.

        - Optionally disable output of decrypted text results and corresponding shift-keys to stdout by toggling :param:`stdout_output` to `False`.

        ---

        :param text: text to be decrypted
        :type text: :class:`str`
        :param stdout_output: toggle structured output of results to stdout, defaults to `True`
        :type stdout_output: :class:`bool`
        :return: dictionary containing all possible pairs of shift-keys and their decrypted results
        :rtype: :class:`dict[str, int]`
        """

        output: dict = {}

        #@ Output all possible shift-keys using the english alphabet
        for key in range(26):

            char_new: str = ''

            for char in text:

                if (char.isupper()):
                    char_new += chr((ord(char) - key - 65) % 26 + 65)

                #@ Decrypt lowercase characters in text
                elif (char.islower()):
                    char_new += chr((ord(char) - key - 97) % 26 + 97)

                #@ Decrypt numbers in text
                elif (char.isdigit()):
                    char_new += str((int(char) - key) % 10)

                #@ Leave all non-alphanumeric characters unchanged.
                else:
                    char_new += char

            if stdout_output:
                print(f'> Decrypted Shift-Key {key} : {char_new}\n')

            #@ Add decrypted text and its corresponding shift-key to dictionary
            output[char_new] = output.get(char_new, (key - 1)) + 1

        return output
