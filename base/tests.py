from django.test import TestCase
from django.contrib.auth.models import User
from .utils.spared_time_counter import count_spared_time, add_spared_time_to_total
from .models import SparedTime


@count_spared_time
def count_zero_duration_function():
    pass


@count_spared_time
def count_time_consuming_function():
    tmp = 0
    for i in range(100000000):
        tmp = i


@count_spared_time
def count_zero_duration_func_with_args(var: str):
    pass


def create_user() -> User:
    user: User = User.objects.create_user('test', 'test')
    SparedTime.objects.create(time=0, teacher=user)
    return user


class TestSparedTimeCounter(TestCase):

    def test_with_zero_function_duration(self):
        """ Should return base 270s if function run quicker than 1s """
        self.assertEqual(count_zero_duration_function(), 270)

    def test_with_time_consuming_function(self):
        """ Should return less spared time than base 270s """
        self.assertLess(count_time_consuming_function(), 270)

    def test_with_arguments(self):
        """ Should can take args to decorator """
        self.assertEqual(count_zero_duration_func_with_args('TEST'), 270)

    def test_total_is_zero_after_create(self):
        """ User should have total 0 of spared time in this app after create """
        user = create_user()
        self.assertEqual(user.sparedtime.time, 0)

    def test_append_spared_time(self):
        """ Time should be added to actual User total spared time in this app """
        user = create_user()
        add_spared_time_to_total(50, user)
        self.assertEqual(user.sparedtime.time, 50)

    def test_no_sparedtime_object_associated(self):
        """ If User has no SparedTime object associated exception should be thrown """
        user = create_user()
        user.sparedtime = None
        user.save()
        with self.assertRaises(AttributeError):
            add_spared_time_to_total(50, user)

    def test_negative_time(self):
        """ If given spared time is negative exception should be thrown. """
        user = create_user()
        with self.assertRaises(ValueError):
            add_spared_time_to_total(-50, user)