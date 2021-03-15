from django.contrib.auth.models import User
from base.models import Department


def create_user():
    user = User.objects.create_user('test', 'test')
    return user


def create_department():
    return Department.objects.create(name='TEST', full_name='TEST')