from django.test import TestCase
from ..set_up_methods import create_user, create_topic_category, create_saved_topic


class TestLessonTopicsView(TestCase):

    def setUp(self) -> None:
        self.user = create_user()

    def test_get_queryset_with_saved_topics(self):
        """ If User has saved topics they should be shown on page. """
        self.client.force_login(self.user)
        category = create_topic_category()
        create_saved_topic(self.user, category)
        create_saved_topic(self.user, category)
        response = self.client.get(path='/saved-topics/')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['saved_topics']), ['<LessonTopic: TOPIC>', '<LessonTopic: TOPIC>'])

    def test_get_queryset_with_no_saved_topics(self):
        """ If User hasn't got any saved topics appropriate message should be shown. """
        self.client.force_login(self.user)
        response = self.client.get(path='/saved-topics/')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['saved_topics']), [])
        self.assertContains(response, 'Aktualnie nie masz żadnych zapisanych tematów.')

    def test_queryset_over_twenty(self):
        """ If queryset is longer than next page button should be shown and next page should be available """
        self.client.force_login(self.user)
        category = create_topic_category()
        for _ in range(21):
            create_saved_topic(self.user, category)
        response = self.client.get(path='/saved-topics/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'next_page_link')
        self.assertContains(response, 'Strona 1 z 2.')

    def test_no_topics_with_given_keyword(self):
        self.client.force_login(self.user)
        response = self.client.get('/saved-topics/?k=test')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nie znaleziono żadnego tematu.')

    def test_topics_with_given_keyword_found(self):
        category = create_topic_category()
        create_saved_topic(self.user, category)
        create_saved_topic(self.user, category)

        self.client.force_login(self.user)
        response = self.client.get('/saved-topics/?k=TOPIC')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['saved_topics']), ['<LessonTopic: TOPIC>', '<LessonTopic: TOPIC>'])

    def test_get_context_data(self):
        self.client.force_login(self.user)
        response = self.client.get('/saved-topics/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(dict(response.context).get('search_form'))