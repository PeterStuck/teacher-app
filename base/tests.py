from django.test import TestCase
from django.contrib.auth.models import User
from .utils.spared_time_counter import count_spared_time, add_spared_time_to_total
from .views import get_user_spared_time
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


class MainNavTest(TestCase):

    def setUp(self) -> None:
        self.user = create_user()

    def test_days_spared_time(self):
        """ Should return actual number of days from User SparedTime object. Page should also show days number. """
        self.user.sparedtime.time = 3600 * 24 + 1
        self.user.sparedtime.save()

        rt = get_user_spared_time(self.user)
        self.client.force_login(self.user)
        response = self.client.get('/menu/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1D')
        self.assertEqual(rt.days, 1)
        self.assertEqual(rt.hours, 0)
        self.assertEqual(rt.minutes, 0)
        self.assertEqual(rt.seconds, 1)

    def test_hour_spared_time(self):
        """ Should return actual number of hours from User SparedTime object. Page should also show hours number. """
        self.user.sparedtime.time = 3600
        self.user.sparedtime.save()

        rt = get_user_spared_time(self.user)
        self.client.force_login(self.user)
        response = self.client.get('/menu/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1G')
        self.assertEqual(rt.hours, 1)
        self.assertEqual(rt.minutes, 0)
        self.assertEqual(rt.seconds, 0)

    def test_minutes_spared_time(self):
        """ Should return actual number of minutes from User SparedTime object. Page should also show minutes number. """
        self.user.sparedtime.time = 60
        self.user.sparedtime.save()

        rt = get_user_spared_time(self.user)
        self.client.force_login(self.user)
        response = self.client.get('/menu/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1M')
        self.assertEqual(rt.hours, 0)
        self.assertEqual(rt.minutes, 1)
        self.assertEqual(rt.seconds, 0)

    def test_seconds_spared_time(self):
        """ Should return actual number of seconds from User SparedTime object. Page should also show seconds number. """
        self.user.sparedtime.time = 15
        self.user.sparedtime.save()

        rt = get_user_spared_time(self.user)
        self.client.force_login(self.user)
        response = self.client.get('/menu/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '15S')
        self.assertEqual(rt.hours, 0)
        self.assertEqual(rt.minutes, 0)
        self.assertEqual(rt.seconds, 15)

    def test_user_with_no_spared_time_obj(self):
        """ Should throw exception if method is invoking with User with no SparedTime object associated """
        self.user.sparedtime = None
        self.user.save()

        with self.assertRaises(AttributeError):
            get_user_spared_time(self.user)

    def test_user_with_zero_time_spared(self):
        """ User with 0 spared time should see appropriate message on page """
        rt = get_user_spared_time(self.user)
        self.client.force_login(self.user)
        response = self.client.get('/menu/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tu widzisz oszczędzony czas.')
        self.assertEqual(rt.days, 0)
        self.assertEqual(rt.hours, 0)
        self.assertEqual(rt.minutes, 0)
        self.assertEqual(rt.seconds, 0)