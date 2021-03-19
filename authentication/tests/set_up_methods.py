from django.contrib.auth.models import User


def create_user() -> User:
    user: User = User.objects.create_user(
        username='test',
        password='test',
        email='test@test.com',
        first_name='TEST',
        last_name='TEST',
        is_active=True
    )
    return user