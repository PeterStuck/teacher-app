from base.utils.auto_str_decorator import auto_str


@auto_str
class FillerVulcanData:
    """ Holds every field that is needed to interact with attendace management on Vulcan """

    def __init__(self, **entries):
        self.__dict__.update(**entries)