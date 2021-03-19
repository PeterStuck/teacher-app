from django.test import TestCase

from revalidation.tests.set_up_methods import create_user, create_department, create_revalidation_student
from revalidation.forms import AddRevalidationStudentForm
from revalidation.models import RevalidationStudent


class TestAddRevalidationStudentForm(TestCase):

    def setUp(self) -> None:
        self.user = create_user()
        self.department = create_department()

    def test_save_with_valid_data(self):
        form = AddRevalidationStudentForm(
            user=self.user,
            instance=create_revalidation_student(self.user, self.department))

        created_student = form.save(
            department_name=self.department.name,
            commit=True)

        self.assertEqual(created_student.department, self.department)
        self.assertQuerysetEqual(
            list(RevalidationStudent.objects.filter(teacher=self.user).all()),
            ['<RevalidationStudent: Test_Name>'])

    def test_save_with_invalid_data(self):
        form = AddRevalidationStudentForm(user=self.user, data={
            'name': 'TEST_NAME',
            'department': None})

        with self.assertRaises(ValueError):
            form.save(department_name=self.department.name, commit=True)