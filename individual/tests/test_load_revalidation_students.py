from django.test import TestCase

from .set_up_methods import create_user, create_department
from ..models import RevalidationStudent


class TestLoadRevalidationStudentsView(TestCase):
    def setUp(self) -> None:
        self.user = create_user()

    def test_with_no_department_sended(self):
        """ If no department was send in GET request, view should return no RevalidationStudents associated with
        user. """
        self.client.force_login(self.user)
        RevalidationStudent.objects.create(name='TEST_STUDENT', department=create_department(), teacher=self.user)
        response = self.client.get('/individual/load_revalidation_students/', data={})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '---')
        self.assertNotContains(response, 'TEST_STUDENT')

    def test_with_no_revalidation_students_associated(self):
        """ If user has no RevalidationStudent object associated view should display only default value of choice: --- """
        self.client.force_login(self.user)
        create_department()
        response = self.client.get('/individual/load_revalidation_students/', data={'department': 'TEST'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '---')

    def test_with_data(self):
        """ If logged user has associated RevalidationStudent objects their names should be display on page """
        self.client.force_login(self.user)
        RevalidationStudent.objects.create(name='TEST_STUDENT', department=create_department(), teacher=self.user)
        response = self.client.get('/individual/load_revalidation_students/', data={'department': 'TEST'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TEST_STUDENT')
