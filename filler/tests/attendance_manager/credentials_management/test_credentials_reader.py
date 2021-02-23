from django.test import TestCase
from filler.attendance_manager.credentials_management.credentials_updater import CredentialsUpdater
from filler.attendance_manager.credentials_management.credentials_reader import CredentialsReader


class TestCredentialsReader(TestCase):
    def setUp(self) -> None:
        self.reader = CredentialsReader()
        self.updater = CredentialsUpdater()
        self.old_credentials = self.reader.get_credentials()

    def tearDown(self) -> None:
        self.updater.update_credentials(self.old_credentials.email, self.old_credentials.password)

    def test_get_credentials(self):
        """ Checks if method return properly credentials from file """
        email = 'email'
        passw = 'passw'

        self.updater.update_credentials(email, passw)

        self.assertEqual(self.reader.get_credentials().email, 'email')
        self.assertEqual(self.reader.get_credentials().password, 'passw')
