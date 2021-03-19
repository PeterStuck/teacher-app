from django.contrib.auth.models import User
from django.test import TestCase

from base.models import Department, LessonTopic, LessonCategory
from revalidation.models import RevalidationStudent
from revalidation.forms import RevalidationLessonForm
from revalidation.views import save_revalidation_topic
from revalidation.tests.set_up_methods import create_user


def create_revalidation_category():
    LessonCategory.objects.create(name='Rewalidacja')


def create_revalidation_lesson_topic(user: User):
    revalidation_category = LessonCategory.objects.get(name__exact='rewalidacja'.title())
    topic = LessonTopic.objects.create(
        topic='Test',
        is_individual=True,
        teacher=user,
        category=revalidation_category
    )

    return topic


class SaveRevalidationTopicTest(TestCase):

    def setUp(self) -> None:
        self.user: User = create_user()
        self.form = RevalidationLessonForm(user=self.user, data={'topic': 'TEST'})
        create_revalidation_category()

    def test_exact_same_topic_already_exists(self):
        """ If given topic is already associated to user then topic shouldn't be saved. """
        create_revalidation_lesson_topic(self.user)
        save_revalidation_topic(self.form, logged_user=self.user)
        self.assertEqual(len(self.user.lessontopic_set.all()), 1)
        self.assertQuerysetEqual(self.user.lessontopic_set.all(), ['<LessonTopic: Test>'])

    def test_save_revalidation_topic(self):
        """ If topic is not associated to logged user already then save the topic. """
        save_revalidation_topic(self.form, logged_user=self.user)
        self.assertEqual(len(self.user.lessontopic_set.all()), 1)
        self.assertQuerysetEqual(self.user.lessontopic_set.all(), ['<LessonTopic: Test>'])