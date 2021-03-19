from base.models import Department
from django.contrib.auth.models import User
from wku_django.settings import BASE_DIR


def create_department():
    return Department.objects.create(
        full_name='Full_Department_Name',
        name='Department')


def create_user() -> User:
    user: User = User.objects.create_user(username='test', password='test', email='test@test.com')
    return user


def create_file():
    with open(BASE_DIR / 'media/teams/test.csv', 'w') as fp:
        for _ in range(5):
            fp.write('TEST TEST TEST TEST\n')