from django.test import TestCase

from authentication.tests.set_up_methods import create_user


class TestChangePassword(TestCase):

    def setUp(self) -> None:
        self.user = create_user()

    def test_change_password_with_correct_actual_password(self):
        """ If old password was correct and new was successfully set then user should be redirected with status = 1 """
        self.client.force_login(self.user)
        response = self.client.post('/change-password/', data={'old_password': 'test', 'new_password': 'new_pass'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account-options?status=1')

    def test_change_password_with_wrong_actual_password(self):
        """ If old password was wrong then user should be redirected with status = 0 """
        self.client.force_login(self.user)
        response = self.client.post('/change-password/', data={'old_password': 'invalid pass', 'new_password': 'new_pass'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account-options?status=0')