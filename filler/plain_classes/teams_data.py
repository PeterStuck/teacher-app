

class TeamsData:
    """ Plain class used as temporary storage for data from teams file """

    def __init__(self, participants: list, actions: list, dates: list):
        assert participants is not None, 'Dataset must be complete!'
        assert actions is not None, 'Dataset must be complete!'
        assert dates is not None, 'Dataset must be complete!'

        self.participants = participants
        self.actions = actions
        self.dates = dates