from datetime import datetime as dt


class VulcanIndividualLessonData:
    """ Plain class to hold initial data to begin app to work """

    def __init__(self,
                 department: str = None,
                 date: dt = None,
                 topic: str = None,
                 comments: str= None,
                 payment_type: str= None,
                 num_of_hours: int= None,
                 presency_status: str= None):
        assert department is not None
        assert date is not None
        assert topic is not None
        assert payment_type is not None
        assert num_of_hours is not None
        assert presency_status is not None

        self.department = department
        self.date = date
        self.topic = topic
        self.comments = comments
        self.payment_type = payment_type
        self.num_of_hours = num_of_hours
        self.presency_status = presency_status
