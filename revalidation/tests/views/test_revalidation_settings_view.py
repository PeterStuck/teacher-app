from django.test import TestCase

from revalidation.tests.set_up_methods import create_user


class TestRevalidationSettingsView(TestCase):

    def setUp(self) -> None:
        self.user = create_user()

    def test_get_context_data(self):
        self.client.force_login(self.user)
        response = self.client.get('/revalidation/settings/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(dict(response.context).get('add_revalidation_student_form'))