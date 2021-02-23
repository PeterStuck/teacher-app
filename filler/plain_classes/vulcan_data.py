

class VulcanData:
    """ Holds every field that is needed to interact with attendace management on Vulcan """

    def __init__(self, file, file_not_loaded, department, day, date, lesson, absent_symbol):
        self.file = file
        self.file_not_loaded = file_not_loaded
        self.department = department
        self.day = day
        self.date = date
        self.lesson = lesson
        self.absent_symbol = absent_symbol