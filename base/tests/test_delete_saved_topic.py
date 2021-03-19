from django.test import TestCase
from .set_up_methods import create_user, create_topic_category, create_saved_topic


class TestDeleteSavedTopic(TestCase):

    def setUp(self) -> None:
        self.user = create_user()

    def test_delete_saved_topic(self):
        """ If some saved topic has given id and it's associated with logged user then topic should be delete """
        self.client.force_login(self.user)
        category = create_topic_category()
        topic = create_saved_topic(self.user, category)
        response = self.client.get(f'/delete-topic/{topic.id}/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(list(self.user.lessontopic_set.all()), [])

    def test_delete_saved_topic_with_wrong_id(self):
        """ When given ID of topic not exists in logged user saved topics set then user should see appropriate message """
        self.client.force_login(self.user)
        response = self.client.get(f'/delete-topic/999/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nie posiadasz w zapisanych tematach pozycji z tym identyfikatorem.')