from base.utils.auto_str_decorator import auto_str


@auto_str
class RevalidationVulcanData:
    """ Plain class to hold initial data to begin app to work """

    def __init__(self,  **entries):
        self.__dict__.update(**entries)

