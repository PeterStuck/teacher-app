from django.test import TestCase
from revalidation.tests.set_up_methods import create_user, create_department
from django.contrib.auth.models import User


class TestSaveRevalidationStudent(TestCase):

    def setUp(self) -> None:
        self.user: User = create_user()
        self.department = create_department()

    def test_save_student_with_valid_data(self):
        self.client.force_login(self.user)
        response = self.client.post('/revalidation/save_revalidation_student/', data={
            'name': 'TEST_NAME',
            'department': self.department.name
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/revalidation/settings/?status=1')
        self.assertQuerysetEqual(list(self.user.revalidationstudent_set.all()), ['<RevalidationStudent: Test_Name>'])

    def test_save_student_with_invalid_data(self):
        self.client.force_login(self.user)
        response = self.client.post('/revalidation/save_revalidation_student/', data={
            'name': 'TEST_NAME',
            'department': 'Not_existing_department'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/revalidation/settings/?status=0')
        self.assertEqual(list(self.user.revalidationstudent_set.all()), [])