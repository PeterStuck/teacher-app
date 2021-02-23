

class UserCredentials:

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def __str__(self):
        return f"Credentials:\n{self.email}\n{self.password}"