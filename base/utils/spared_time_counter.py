from time import time
from django.contrib.auth.models import User


def count_spared_time(func):
    """ Counts spared time with one of the apps.
        * 5 min -> 300s is average time of filling up data in Vulcan by Teacher manually.
        * 30s is time that takes to set up app.
    """
    def func_wrapper(*args):
        start = time()
        func(*args)
        stop = time()
        func_duration = int(stop - start)
        return 300 - 30 - func_duration

    return func_wrapper


def add_spared_time_to_total(time_in_sec: int, user: User):
    __check_time_no_negative(time_in_sec)
    if hasattr(user, 'sparedtime'):
        user.sparedtime.time += time_in_sec
        user.sparedtime.save()
    else:
        raise AttributeError("User has no SparedTime object associated")


def __check_time_no_negative(time: int):
    if time < 0:
        raise ValueError("Spared time cannot be negative!")