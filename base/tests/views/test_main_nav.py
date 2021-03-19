from django.test import TestCase
from base.tests.set_up_methods import create_user
from base.views import get_user_spared_time


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