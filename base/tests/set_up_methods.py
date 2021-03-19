from django.contrib.auth.models import User
from base.models import LessonTopic, LessonCategory, SparedTime


def create_user() -> User:
    user: User = User.objects.create_user('test', 'test')
    SparedTime.objects.create(time=0, teacher=user)
    return user


def create_topic_category():
    category = LessonCategory.objects.create(
        name='CATEGORY'
    )
    return category


def create_saved_topic(teacher, category):
    saved_topic = LessonTopic.objects.create(
        topic='TOPIC',
        is_individual=True,
        teacher=teacher,
        category=category
    )
    return saved_topic