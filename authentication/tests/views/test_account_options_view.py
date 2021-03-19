from django.test import TestCase

from authentication.tests.set_up_methods import create_user


class TestAccountOptionsView(TestCase):

    def setUp(self) -> None:
        self.user = create_user()

    def test_get_context_data(self):
        self.client.force_login(self.user)
        response = self.client.get('/account-options/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(dict(response.context).get('change_password_form'))
