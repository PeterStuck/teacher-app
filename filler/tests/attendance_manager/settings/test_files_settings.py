from django.test import TestCase
from filler.attendance_manager.settings.files_settings import FilesSettings


class TestFilesSettings(TestCase):
    def setUp(self) -> None:
        self.settings = FilesSettings()
        self.old_data = self.settings.load_settings()

    def tearDown(self) -> None:
        self.settings.update_settings(self.old_data)

    def test_load_settings(self):
        """ Checks if loaded config is same as set before """
        new_config = {
            'path': 'Some path',
            'other_path': 'Some other path'
        }
        self.settings.update_settings(new_config)
        self.assertEqual(self.settings.load_settings(), new_config)

    def test_update_settings(self):
        """ Checks if current config after update is different from old one """
        new_config = {
            'path': 'Some path',
            'other_path': 'Some other path'
        }
        self.settings.update_settings(new_config)
        self.assertNotEqual(self.settings.load_settings(), self.old_data)
        self.assertEqual(self.settings.load_settings(), new_config)
