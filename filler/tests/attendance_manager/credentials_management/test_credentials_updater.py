from django.test import TestCase
from filler.attendance_manager.credentials_management.credentials_updater import CredentialsUpdater
from filler.attendance_manager.credentials_management.credentials_reader import CredentialsReader
from filler.plain_classes.user_credentials import UserCredentials


class TestCredentialsUpdater(TestCase):
    def setUp(self) -> None:
        self.reader = CredentialsReader()
        self.updater = CredentialsUpdater()
        self.old_credentials = self.reader.get_credentials()

    def tearDown(self) -> None:
        self.updater.update_credentials(self.old_credentials.email, self.old_credentials.password)

    def test_update_credentials(self):
        """ Checks if credentials were updated """
        new_credentials = UserCredentials(email='Email', password='Pass')
        self.updater.update_credentials(new_credentials.email,  new_credentials.password)

        self.assertEqual(self.reader.get_credentials().email, new_credentials.email)
        self.assertEqual(self.reader.get_credentials().password, new_credentials.password)
        self.assertNotEqual(self.reader.get_credentials(), self.old_credentials)
