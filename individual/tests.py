from django.test import TestCase
from django.contrib.auth.models import User
from .plain_classes.vulcan_data import VulcanIndividualLessonData
from base.models import Department
from .models import RevalidationStudent


class VulcanIndividualLessonDataTest(TestCase):
    def setUp(self):
        self.vulcan_data = None

    def test_department_not_none(self):
        with self.assertRaises(AssertionError):
            self.vulcan_data = VulcanIndividualLessonData(department=None)

    def test_date_not_none(self):
        with self.assertRaises(AssertionError):
            self.vulcan_data = VulcanIndividualLessonData(date=None)

    def test_topic_not_none(self):
        with self.assertRaises(AssertionError):
            self.vulcan_data = VulcanIndividualLessonData(topic=None)

    def test_payment_type_not_none(self):
        with self.assertRaises(AssertionError):
            self.vulcan_data = VulcanIndividualLessonData(payment_type=None)

    def test_num_of_hours_not_none(self):
        with self.assertRaises(AssertionError):
            self.vulcan_data = VulcanIndividualLessonData(num_of_hours=None)

    def test_presency_status_not_none(self):
        with self.assertRaises(AssertionError):
            self.vulcan_data = VulcanIndividualLessonData(presency_status=None)


def create_user():
    user = User.objects.create_user('test', 'test')
    return user


def create_department():
    return Department.objects.create(name='TEST', full_name='TEST')


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