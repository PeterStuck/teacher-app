from django.test import TestCase
from base.tests.set_up_methods import create_user


class TestEndOfWorkView(TestCase):

    def setUp(self) -> None:
        self.user = create_user()

    def test_end_of_work_view(self):
        self.client.force_login(self.user)
        response = self.client.get(path='/eow/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Uzupełnianie zakończone. Masz wolne. Przynajmniej na chwilę. 😉')
