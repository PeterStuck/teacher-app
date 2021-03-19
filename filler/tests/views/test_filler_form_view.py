from django.test import TestCase
from filler.tests.set_up_methods import create_department, create_user, create_file
from wku_django.settings import BASE_DIR
import os
from filler.views import save_file


class TestFillerFormView(TestCase):

    def setUp(self) -> None:
        self.department = create_department()
        self.user = create_user()
        self.ufn = '2020-01-01-Department-1.csv'
        self.tfn = 'test.csv'

    def tearDown(self) -> None:
        """ Removes files created in tests """
        uploaded_file_path = str(BASE_DIR / f'media/teams/{self.ufn}')
        test_file_path = str(BASE_DIR / f'media/teams/{self.tfn}')

        if os.path.isfile(uploaded_file_path):
            os.remove(uploaded_file_path)

        if os.path.isfile(test_file_path):
            os.remove(test_file_path)

    def test_form_when_file_not_given_and_checkbox_not_checked(self):
        """ If user doesn't pass file to form and has not check file_not_loaded checkbox then appropriate message should be shown. """
        self.client.force_login(self.user)
        response = self.client.post('/filler/', data={
            'teams_file': '',
            'file_not_loaded': False,
            'departments': self.department.name,
            'day': 'Poniedziałek',
            'date': '2020-01-01',
            'lesson': '1',
            'is_double_lesson': False,
            'absent_symbol': '▬'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Musisz wgrać plik lub wybrać opcję jednakowej obecności, aby program mógł przystąpić do działania.')

    def test_save_file(self):
        create_file()
        file_path = str(BASE_DIR / 'media/teams/test.csv')
        with open(file_path, 'r') as file:
            save_file(self.ufn, file)

        expected_file_path = str(BASE_DIR / f'media/teams/{self.ufn}')
        self.assertTrue(os.path.isfile(file_path))
        self.assertTrue(os.path.isfile(expected_file_path))