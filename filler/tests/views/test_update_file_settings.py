from django.test import TestCase
from filler.tests.set_up_methods import create_user
from filler.attendance_manager.settings.files_settings import FilesSettings


class TestUpdateFilesSettings(TestCase):

    def setUp(self) -> None:
        self.user = create_user()
        self.old_data = FilesSettings().load_settings()

    def tearDown(self) -> None:
        FilesSettings().update_settings(self.old_data)

    def test_successfully_update_file_settings(self):
        previous_archive_path = self.old_data['archive_desktop_path']

        self.client.force_login(self.user)
        response = self.client.post('/filler/settings/update_files/', data={
            'archive_desktop_path': 'New_test_path'
        })

        settings = FilesSettings().load_settings()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/filler/settings?status=1')
        self.assertEqual(settings['archive_desktop_path'], 'New_test_path')
        self.assertNotEqual(settings['archive_desktop_path'], previous_archive_path)

    def test_update_files_settings_with_invalid_data(self):
        previous_archive_path = self.old_data['archive_desktop_path']

        self.client.force_login(self.user)
        response = self.client.post('/filler/settings/update_files/', data={
            'archive_desktop_path': ''
        })

        settings = FilesSettings().load_settings()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/filler/settings?status=0')
        self.assertEqual(settings['archive_desktop_path'], previous_archive_path)