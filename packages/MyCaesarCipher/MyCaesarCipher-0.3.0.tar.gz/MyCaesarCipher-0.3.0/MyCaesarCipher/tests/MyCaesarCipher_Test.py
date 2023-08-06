from typing import Any
from MyCaesarCipher.main import CaesarCipher


class CaesarCipherTesting:

    def __init__(self, test_class=CaesarCipher()) -> None:
        self.test_class: Any = test_class

    def test_encrypt(
        self,
        text: str,
        key: int,
        assertion: str,
        output_results: bool = True,
    ) -> None:
        """
        Tests encryption of given text and shift-key and asserts the result
        is equal to the output.

        :param text: text to encrypt
        :type text: :class:`str`
        :param key: key to use for encryption
        :type key: :class:`str` | `None`
        :param assertion: expected output of the encryption
        :type assertion: :class:`str`
        :param output_results: toggle result output, defaults to :bool:`True`
        :type output_results: :class:`bool` (optional)
        """

        assert self.test_class.encrypt(text, key, output_results) == assertion

    def test_decrypt(self,
                     text: str,
                     assertion: str,
                     output_results: bool = False) -> None:
        """
        Tests decryption of given text and whether the assertion can be found within resulting output.

        ---

        :param text: the text to be decrypted
        :type text: :class:`str`
        :param assertion: expected result to be found within output
        :type assertion: :class:`str`
        :param output_results: toggle output of results to `stdout`, defaults to `False`
        :type output_results: :class:`bool` (optional)
        """

        assert assertion in self.test_class.decrypt(text, output_results)


# Create test class instance.
testCC: CaesarCipherTesting = CaesarCipherTesting()


# Test encryption of string containing 5 uppercase characters.
def test_encodeA() -> None:
    testCC.test_encrypt('TESTING', 5, 'YJXYNSL')


# Test encryption of string containing both lowercase and uppercase characters.
def test_encodeB() -> None:
    testCC.test_encrypt("TeStInG", 5, 'YjXyNsL')


# Test encryption of string containing digits.
def test_encodeC() -> None:
    testCC.test_encrypt('16', 5, '61')


# Test encryption of string containing lowercase/uppercase characters and digits.
def test_encodeD() -> None:
    testCC.test_encrypt("Password123", 5, 'Ufxxbtwi678', False)


def test_decodeA() -> None:
    testCC.test_decrypt('1djjktcqttccwprztsd', '0syyzirfiirrlegoihs')


def test_decodeB() -> None:
    testCC.test_decrypt('2ekkludruuddxosaute', '1djjktcqttccwnrztsd')
