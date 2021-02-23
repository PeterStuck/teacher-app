from filler.attendance_manager.settings.settings import Settings
from django.test import TestCase


class TestSettings(TestCase):
    def setUp(self) -> None:
        self.settings = Settings()

    def test_main_config_file_exists(self):
        """ Checks if main config file is not empty and exists """
        self.assertNotEqual(self.settings.load_main_settings(), None)

