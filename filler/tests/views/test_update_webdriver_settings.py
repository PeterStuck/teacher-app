from django.test import TestCase
from filler.tests.set_up_methods import create_user
from filler.attendance_manager.settings.webdriver_settings import WebdriverSettings


class TestUpdateWebdriverSettings(TestCase):

    def setUp(self) -> None:
        self.user = create_user()
        self.old_data = WebdriverSettings().load_settings()

    def tearDown(self) -> None:
        WebdriverSettings().update_settings(self.old_data)

    def test_successfully_update_webdriver_settings(self):
        previous_vulcan_url = self.old_data['vulcan_url']

        self.client.force_login(self.user)
        response = self.client.post('/filler/settings/update_webdriver/', data={
            'vulcan_url': 'New_Vulcan_URL'
        })

        settings = WebdriverSettings().load_settings()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/filler/settings?status=1')
        self.assertEqual(settings['vulcan_url'], 'New_Vulcan_URL')
        self.assertNotEqual(settings['vulcan_url'], previous_vulcan_url)

    def test_update_files_settings_with_invalid_data(self):
        previous_vulcan_url = self.old_data['vulcan_url']

        self.client.force_login(self.user)
        response = self.client.post('/filler/settings/update_webdriver/', data={
            'vulcan_url': ''
        })

        settings = WebdriverSettings().load_settings()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/filler/settings?status=0')
        self.assertEqual(settings['vulcan_url'], previous_vulcan_url)