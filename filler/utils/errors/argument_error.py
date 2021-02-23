

class InvalidArgumentError(Exception):

    def __init__(self, argument, message='Given argument is wrong.'):
        self.argument = argument
        self.message = message
        super().__init__(self.message)