from django.test import TestCase

from ..set_up_methods import create_user


class TestLoginFormView(TestCase):

    def setUp(self) -> None:
        self.user = create_user()

    def test_get_context_data(self):
        response = self.client.get(path='/login/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(dict(response.context).get('login_form'))

    def test_get_when_user_is_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(path='/login/')

        self.assertTrue(self.user.is_authenticated)
        self.assertEqual(response.status_code, 302)

    def test_get_when_user_is_not_authenticated(self):
        response = self.client.get(path='/login/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(dict(response.context).get('login_form'))

    def test_form_valid_and_credentials_correct(self):
        """ If credentials was correct user should be redirected and variable with credentials should be added to session """
        response = self.client.post('/login/', data={'email': self.user.email, 'password': 'test'})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.is_authenticated)
        self.assertEqual(self.client.session['credentials'], {'email': self.user.email, 'password': 'test'})

    def test_login_with_invalid_email(self):
        """ When user passes email that not exists in database then stay at login page """
        response = self.client.post('/login/', data={'email': 'invalid email', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(dict(response.context).get('login_form'))

    def test_login_with_invalid_password(self):
        response = self.client.post('/login/', data={'email': self.user.email, 'password': 'invalid password'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(dict(response.context).get('login_form'))

    def test_redirect_to_next_parameter(self):
        """ When next parameter is provided then user after successfully login should be redirected to page with next url """
        response = self.client.post('/login/', data={'email': self.user.email, 'password': 'test', 'next': '/eow/'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/eow/')

    def test_redirect_without_next_parameter(self):
        """ If there is no next parameter provided user should be redirected to /menu/ by default """
        response = self.client.post('/login/', data={'email': self.user.email, 'password': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/menu/')