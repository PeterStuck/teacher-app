from django.test import TestCase
from filler.tests.set_up_methods import create_user
from filler.attendance_manager.settings import files_settings, webdriver_settings
from wku_django.settings import BASE_DIR


class TestSettingsView(TestCase):

    def setUp(self) -> None:
        self.user = create_user()

    def get_response_from_settings_view(self):
        self.client.force_login(self.user)
        return self.client.get('/filler/settings/')

    def test_get_context_data(self):
        self.client.force_login(self.user)
        response = self.client.get('/filler/settings/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(dict(response.context).get('archive_form'))
        self.assertTrue(dict(response.context).get('webdriver_form'))

    def test_prepopulate_archive_form(self):
        settings = files_settings.FilesSettings().load_settings()
        expeceted_archive_path = str(BASE_DIR / settings['archive_desktop_path'])

        response = self.get_response_from_settings_view()

        archive_form = dict(response.context).get('archive_form')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(expeceted_archive_path in str(archive_form['archive_desktop_path']))

    def test_prepopulate_webdriver_form(self):
        settings = webdriver_settings.WebdriverSettings().load_settings()
        expeceted_vulcan_url = settings['vulcan_url']

        response = self.get_response_from_settings_view()

        webdriver_form = dict(response.context).get('webdriver_form')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(expeceted_vulcan_url in str(webdriver_form['vulcan_url']))