from filler.plain_classes.user_credentials import UserCredentials
from filler.utils.security.caesar_cypher import CaesarCypher


class CredentialsReader:

    def get_credentials(self) -> UserCredentials:
        """ Returns decoded credentials """
        with open(r'D:\Projekty\Python\wku_django\filler\static\files\entry.txt', 'r') as credentials:
            data = credentials.readlines()
            encoded_email = data[0]
            encoded_pass = data[1]
            shifts = data[2].split()
            salting = data[3]

        return self.__decode_credentials(encoded_email, encoded_pass, shifts, salting)

    def __decode_credentials(self, encoded_email, encoded_pass, shifts, salting) -> UserCredentials:
        cypher = CaesarCypher()
        decoded_email = encoded_email
        decoded_pass = encoded_pass
        for shift in reversed(shifts):
            cypher.shift = int(shift)
            decoded_email = cypher.decode(decoded_email)
            decoded_pass = cypher.decode(decoded_pass)

        email = cypher.remove_salting(decoded_email, salting)
        passw = cypher.remove_salting(decoded_pass, salting)
        return UserCredentials(email=email, password=passw)