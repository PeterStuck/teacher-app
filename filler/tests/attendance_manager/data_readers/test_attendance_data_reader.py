from django.test import TestCase
from filler.utils.errors.argument_error import InvalidArgumentError
from filler.plain_classes.teams_data import TeamsData
from filler.attendance_manager.settings.files_settings import FilesSettings
from filler.attendance_manager.data_readers.attendance_data_reader import AttendanceDataReader

from wku_django.settings import BASE_DIR

import os
import glob


def create_teams_data():
    participants = ['Test1', 'Test2', 'Test3']
    actions = ['Test', 'Test', 'Test']
    dates = ['Test', 'Test', 'Test']
    return TeamsData(participants=participants, actions=actions, dates=dates)


class TestAttendanceDataReader(TestCase):
    def setUp(self) -> None:
        self.adr = AttendanceDataReader()
        self.settings = FilesSettings()
        self.settings_dict = self.settings.load_settings()
        self.filename = 'test.csv'

    def tearDown(self) -> None:
        """ Removes files created in tests """
        converted_file_path = str(BASE_DIR / self.settings_dict['coverted_files_path']) + "\\" + self.filename
        archive_file_path = self.settings_dict['archive_desktop_path'] + "\\" + self.filename
        raw_file_path = str(BASE_DIR / self.settings_dict['raw_teams_file_path']) + "\\" + self.filename

        if os.path.isfile(converted_file_path):
            os.remove(converted_file_path)

        if os.path.isfile(archive_file_path):
            os.remove(archive_file_path)

        if os.path.isfile(raw_file_path):
            os.remove(raw_file_path)

    def test_convert_teams_file(self):
        """ Checks creating files on archive and converted directories. """
        basePath = BASE_DIR / self.settings_dict["raw_teams_file_path"]
        filePaths = glob.glob(os.path.join(basePath, '*.csv'))

        with open(filePaths[0], 'r') as file:
            with open(str(basePath) + "\\" + self.filename, 'w', encoding='utf16') as test_file:
                for line in file.readlines()[:-1]:
                    test_file.write(line)

        self.adr.convert_teams_file(self.filename)

        self.assertTrue(os.path.isfile(str(BASE_DIR / self.settings_dict['coverted_files_path']) + "\\" + self.filename))
        self.assertTrue(os.path.isfile(self.settings_dict['archive_desktop_path'] + '\\' + self.filename))

    def test_recreate_csv_file(self):
        """ Test is able to recreate csv file based on data from Teams """
        td = create_teams_data()

        self.adr.recreate_csv_file(td, filename=self.filename)

        self.assertEqual(self.adr.get_participants(self.filename), set(td.participants))
        self.assertEqual(os.path.isfile(self.settings_dict['coverted_files_path'] + self.filename), True)

    def test_recreate_csv_file_with_none(self):
        """ Should throw exception when try to recreate file based on None """
        with self.assertRaises(InvalidArgumentError):
            self.adr.recreate_csv_file(None, filename=self.filename)

    def test_get_participants(self):
        """ Checks if converted file is in right format """
        td = create_teams_data()

        self.adr.recreate_csv_file(td, filename=self.filename)
        self.assertEqual(self.adr.get_participants(self.filename), set(td.participants))
