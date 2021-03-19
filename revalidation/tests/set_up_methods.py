from django.contrib.auth.models import User
from base.models import Department
from revalidation.models import RevalidationStudent, IndividualLessonPaymentType


def create_user(username=None):
    if username:
        return User.objects.create_user(username, 'test')
    user = User.objects.create_user('test', 'test')
    return user


def create_department():
    return Department.objects.create(name='TEST', full_name='TEST')


def create_revalidation_student(user, department):
    return RevalidationStudent.objects.create(
        teacher=user,
        department=department,
        name='TEST_NAME'
    )

def create_payment_type():
    return IndividualLessonPaymentType.objects.create(type='TEST_TYPE')