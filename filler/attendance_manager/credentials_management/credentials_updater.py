from filler.utils.security.caesar_cypher import CaesarCypher


class CredentialsUpdater:

    def update_credentials(self, plain_email: str, plain_pass: str):
        encoded_email, encoded_pass = self.__crypt_credentials(plain_email, plain_pass)
        actual_data = self.__get_actual_data()

        actual_data[0] = encoded_email + "\n"
        actual_data[1] = encoded_pass + "\n"

        self.__save_changes(actual_data)

    def __crypt_credentials(self, plain_email: str, plain_pass: str):
        shifts, salting = self.__get_crypt_parameters()
        cypher = CaesarCypher()

        cypher.shift = int(shifts[0])
        encoded_email = cypher.encode(plain_email)
        encoded_pass = cypher.encode(plain_pass)

        encoded_email = cypher.add_salting(encoded_email, salting)
        encoded_pass = cypher.add_salting(encoded_pass, salting)

        cypher.shift = int(shifts[1])
        encoded_email = cypher.encode(encoded_email)
        encoded_pass = cypher.encode(encoded_pass)

        return encoded_email, encoded_pass

    def __get_actual_data(self):
        with open(r'D:\Projekty\Python\wku_django\filler\static\files\entry.txt', 'r') as credentials:
            data = credentials.readlines()
        return data

    def __get_crypt_parameters(self):
        data = self.__get_actual_data()
        shifts = data[2].split()
        salting = data[3]
        return shifts, salting

    def __save_changes(self, new_data):
        with open(r'D:\Projekty\Python\wku_django\filler\static\files\entry.txt', 'w') as credentials:
            for single_data in new_data:
                credentials.write(single_data)