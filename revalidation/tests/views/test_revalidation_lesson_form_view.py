from datetime import datetime

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from selenium.webdriver import Chrome

from revalidation.tests.set_up_methods import create_user, log_in_into_app


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


class TestRevalidationIndexViewLive(StaticLiveServerTestCase):

    def setUp(self) -> None:
        self.user = create_user()
        self.agent = None

    def get_comments_value(self, id_comments):
        return self.agent.execute_script(f"""return document.querySelector('#{id_comments}').value;""")

    def test_comments_shortcut_buttons(self):
        self.agent = Chrome(executable_path='D:\Projekty\Python\wku_django\webdriver\chromedriver.exe')
        self.agent.get(f'{self.live_server_url}/revalidation/')

        log_in_into_app(self.agent)

        id_comments = 'id_comments'
        shortcut_buttons = self.agent.find_elements_by_css_selector('.comments_shortcut button')

        shortcut_buttons[0].click()
        self.assertEqual(self.get_comments_value(id_comments), 'MS Teams. Zajęcia dostosowane do możliwości i potrzeb ucznia.')

        shortcut_buttons[1].click()
        self.assertEqual(self.get_comments_value(id_comments), 'MS Teams. Zajęcia dostosowane do możliwości i potrzeb uczennicy.')

        shortcut_buttons[2].click()
        self.assertEqual(self.get_comments_value(id_comments), 'Zajęcia stacjonarne.')