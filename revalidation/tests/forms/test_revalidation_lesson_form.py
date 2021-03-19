from django.test import TestCase

from revalidation.tests.set_up_methods import create_user, create_department, create_revalidation_student, create_payment_type
from revalidation.forms import RevalidationLessonForm


class TestRevalidationLessonForm(TestCase):

    def setUp(self) -> None:
        self.user = create_user()
        self.department = create_department()

    def get_prepopulated_form(self, student, user):
        return RevalidationLessonForm(user=user, data={
            'department': self.department.name,
            'student': student.id,
            'date': '01.01.2020',
            'topic': 'Test_TOPIC',
            'get_saved_topic': False,
            'payment_type': create_payment_type().type,
            'num_of_hours': 1,
            'presence_symbol': '▬'
        })

    def test_dependend_student_department(self):
        student = create_revalidation_student(self.user, self.department)
        valid_form = self.get_prepopulated_form(student, self.user)

        another_teacher = create_user(username='another')
        student_form_teacher = create_revalidation_student(another_teacher, self.department)
        invalid_form = self.get_prepopulated_form(student_form_teacher, self.user)

        self.assertTrue(valid_form.is_valid())
        self.assertFalse(invalid_form.is_valid())

    def test_parse_to_vulcan_data(self):
        student = create_revalidation_student(self.user, self.department)
        valid_form = self.get_prepopulated_form(student, self.user)

        valid_form.is_valid()
        vd = valid_form.parse_to_vulcan_data()

        self.assertEqual(str(vd), 'RevalidationVulcanData(department=TEST, student=TEST_NAME, date=01.01.2020, topic=Test_TOPIC, get_saved_topic=False, comments=None, payment_type=TEST_TYPE, num_of_hours=1, presence_symbol=▬)')
