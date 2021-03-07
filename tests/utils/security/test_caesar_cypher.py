from django.test import TestCase

from utils.security.caesar_cypher import CaesarCypher, ALL_UPPERCASE_LETTERS
from filler.utils.errors.argument_error import InvalidArgumentError


class TestCaesarCypher(TestCase):
    def setUp(self) -> None:
        self.cypher = CaesarCypher()
        self.cypher.shift = 5

    def test_encode(self):
        """ Should encode entire word with given shift """
        test_word = 'TEST'
        encoded_word = self.cypher.encode(word=test_word)
        self.assertEqual(encoded_word, 'YJXY')

    def test_encode_character(self):
        """ Should change individual character into shifted char """
        test_char = 'A'
        encoded_char = self.cypher.encode_character(letter=test_char, collection=ALL_UPPERCASE_LETTERS)
        self.assertEqual(encoded_char, 'F')

    def test_encode_character_none_collection(self):
        """ Passed None as collection into method should result with InvalidArgumentError """
        test_char = 'A'
        with self.assertRaises(InvalidArgumentError):
            self.cypher.encode_character(letter=test_char)

    def test_decode(self):
        """ Should be able to decode word when shift is known """
        encoded_word = self.cypher.decode('YJXY')
        self.assertEqual(encoded_word, 'TEST')

    def test_decode_character(self):
        """ Should decode given character using shift reversed way """
        encoded_char = 'F'
        self.assertEqual(self.cypher.decode_character(letter=encoded_char, collection=ALL_UPPERCASE_LETTERS), 'A')

    def test_decode_character_none_collection(self):
        """ If passed collection is None, InvalidArgumentError should be raised """
        encoded_char = 'F'
        with self.assertRaises(InvalidArgumentError):
            self.cypher.decode_character(letter=encoded_char)

    def test_add_salting(self):
        """ Should return word with encoded salting at start """
        salt = 'AAAA'
        word = 'TEST'
        salted_word = self.cypher.add_salting(word=word, salt=salt)
        self.assertEqual(salted_word, 'FFFFTEST')

    def test_remove_salting(self):
        """ Should remove salting from decoded word """
        encoded_word = self.cypher.encode(word='TEST')
        salt = 'AAA'
        salted_word = self.cypher.add_salting(word=encoded_word, salt=salt)
        decoded_word = self.cypher.decode(salted_word)
        self.assertEqual(self.cypher.remove_salting(decoded_word, salt), 'TEST')

    def test_remove_salting_with_wrong_salt_pattern(self):
        """ If given salt pattern does not match the salt from the word, appropriate exception will be thrown."""
        encoded_word = self.cypher.encode(word='TEST')
        salt = 'AAA'
        salted_word = self.cypher.add_salting(word=encoded_word, salt=salt)
        decoded_word = self.cypher.decode(salted_word)
        with self.assertRaises(InvalidArgumentError):
            self.cypher.remove_salting(word=decoded_word, salt='BBB')