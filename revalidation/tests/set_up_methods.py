from django.contrib.auth.models import User
import time
from base.models import Department
from revalidation.models import RevalidationStudent, IndividualLessonPaymentType


def create_user(username=None):
    if username:
        return User.objects.create_user(username, 'test')
    user = User.objects.create_user(email='test', username='test', password='test')
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


def log_in_into_app(agent):
    email = agent.find_element_by_name('email')
    password = agent.find_element_by_name('password')

    email.send_keys('test')
    password.send_keys('test')
    agent.find_element_by_class_name('submit_btn').click()
    time.sleep(1)