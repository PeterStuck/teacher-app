from datetime import datetime

from django.test import TestCase

from revalidation.tests.set_up_methods import create_user


class TestRevalidationLessonFormView(TestCase):

    def setUp(self) -> None:
        self.user = create_user()

    def test_get_context_data(self):
        self.client.force_login(self.user)
        response = self.client.get('/revalidation/')

        form = dict(response.context).get('revalidation_lesson_form')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(form)
        self.assertTrue(datetime.now().strftime('%d.%m.%Y') in str(form['date']))

    def test_form_invalid(self):
        self.client.force_login(self.user)
        response = self.client.post('/revalidation/', data={})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(dict(response.context).get('revalidation_lesson_form'))
        self.assertContains(response, 'error')