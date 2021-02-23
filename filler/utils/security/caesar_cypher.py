from string import ascii_uppercase, ascii_lowercase, digits, punctuation
from math import fabs

from ..errors.argument_error import InvalidArgumentError

ALL_LOWERCASE_LETTERS = ascii_lowercase
ALL_UPPERCASE_LETTERS = ascii_uppercase
ALL_SYMBOLS = punctuation
ALL_DIGITS = digits


class CaesarCypher:
    """ Simple crypt algorithm class """
    
    def __init__(self):
        self.shift = 0

    def encode(self, word: str) -> str:
        """ Encode word into caesar cipher crypt with given shift """
        encoded_word = ""

        for letter in word:
            if letter in ALL_SYMBOLS:
                encoded_word += self.encode_character(letter=letter, collection=ALL_SYMBOLS)
            elif letter in ALL_LOWERCASE_LETTERS:
                encoded_word += self.encode_character(letter=letter, collection=ALL_LOWERCASE_LETTERS)
            elif letter in ALL_UPPERCASE_LETTERS:
                encoded_word += self.encode_character(letter=letter, collection=ALL_UPPERCASE_LETTERS)
            elif letter in ALL_DIGITS:
                encoded_word += self.encode_character(letter=letter, collection=ALL_DIGITS)

        return encoded_word

    def encode_character(self, letter: str, collection: list = None) -> str:
        """ Encode single ASCII character into caesar cipher crypt with given shift """
        if collection is None:
            raise InvalidArgumentError(message="Collection can't be of type None", argument=collection)

        index = collection.index(letter)
        new_index = index + self.shift
        if new_index > len(collection) - 1:
            new_index = (new_index % len(collection))
            return collection[new_index]
        else:
            return collection[new_index]

    def decode(self, word: str) -> str:
        """ Decode word from caesar cipher crypt with given shift """
        decoded_word = ""

        for letter in word:
            if letter in ALL_SYMBOLS:
                decoded_word += self.decode_character(letter=letter, collection=ALL_SYMBOLS)
            elif letter in ALL_LOWERCASE_LETTERS:
                decoded_word += self.decode_character(letter=letter, collection=ALL_LOWERCASE_LETTERS)
            elif letter in ALL_UPPERCASE_LETTERS:
                decoded_word += self.decode_character(letter=letter, collection=ALL_UPPERCASE_LETTERS)
            elif letter in ALL_DIGITS:
                decoded_word += self.decode_character(letter=letter, collection=ALL_DIGITS)

        return decoded_word

    def decode_character(self, letter: str, collection: list = None) -> str:
        """ Decode single character from caesar cipher crypt into ASCII character with given shift """
        if collection is None:
            raise InvalidArgumentError(message="Collection can't be of type None", argument=collection)

        index = collection.index(letter)
        new_index = index - self.shift
        if new_index < 0:
            new_index = int(fabs(new_index % len(collection)))
            return collection[new_index]
        else:
            return collection[new_index]

    def add_salting(self, word: str, salt: str) -> str:
        """ Takes currently encoded word and adds at start encoded salting pattern """
        encoded_salt = self.encode(salt)
        return (encoded_salt + word).strip()

    def remove_salting(self, word: str, salt: str) -> str:
        """ Removes salting pattern from decoded word. Salt must be known to remove. """
        salt = salt.replace("\n", "")
        word_without_salt = word.replace(salt, "")
        if len(word_without_salt) == len(word):
            raise InvalidArgumentError('Salt pattern is wrong.')
        return word_without_salt