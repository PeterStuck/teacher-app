from django.test import TestCase

from authentication.tests.set_up_methods import create_user


class TestLogoutView(TestCase):

    def setUp(self) -> None:
        self.user = create_user()

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.get('/logout/')
        response_menu = self.client.get('/menu/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response_menu.status_code, 302)
        self.assertEqual(response_menu.url, '/login?next=/menu/')