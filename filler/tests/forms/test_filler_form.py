from django.test import TestCase

from filler.forms import FillerForm
from filler.tests.set_up_methods import create_department, create_user, create_file
from wku_django.settings import BASE_DIR
import os


class TestFillerForm(TestCase):

    def setUp(self) -> None:
        self.department = create_department()
        self.user = create_user()

    def tearDown(self) -> None:
        test_file_path = str(BASE_DIR / f'media/teams/test.csv')

        if os.path.isfile(test_file_path):
            os.remove(test_file_path)

    def test_parse_to_vulcan_data(self):
        form = FillerForm({
            'teams_file': None,
            'file_not_loaded': True,
            'departments': self.department.name,
            'day': 'Poniedziałek',
            'date': '2020-01-01',
            'lesson': '1',
            'is_double_lesson': False,
            'absent_symbol': '▬'
        })

        form.is_valid()
        vd = form.parse_to_vulcan_data()
        self.assertTrue(form.is_valid())
        self.assertEqual(str(vd), f'FillerVulcanData(teams_file=None, file_not_loaded=True, departments={self.department.name}, day=Poniedziałek, date=2020-01-01, lesson=1, is_double_lesson=False, absent_symbol=▬, filename=None)')

    def test_determine_filename_with_no_file(self):
        form = FillerForm({
            'teams_file': '',
            'file_not_loaded': True,
            'departments': self.department.name,
            'day': 'Poniedziałek',
            'date': '2020-01-01',
            'lesson': '1',
            'is_double_lesson': False,
            'absent_symbol': '▬'
        })

        form.is_valid()
        vd = form.parse_to_vulcan_data()

        self.assertTrue(form.is_valid())
        self.assertEqual(vd.filename, None)
