from django.contrib import admin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.test import TestCase, override_settings
from django.urls import path, include
from django.views.generic.base import RedirectView



def response_error_500(request):
    return render(request, 'error_pages/500.html', status=500)


urlpatterns = [
    path('', include('authentication.urls')),
    path('', include('base.urls')),
    path('filler/', include('filler.urls')),
    path('revalidation/', include('revalidation.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login', permanent=True)),
    path('500/', response_error_500)
]


def create_user() -> User:
    user: User = User.objects.create_user('test', 'test')
    return user


class CustomErrorHandlerTests(TestCase):

    def setUp(self) -> None:
        self.user = create_user()

    def test_handler_renders_template_response(self):
        self.client.force_login(self.user)
        response = self.client.get('/this-page-not-exists/')

        self.assertEqual(response.status_code, 404)
        self.assertTrue('Nie znaleziono strony.' in str(response.content))

    @override_settings(ROOT_URLCONF=__name__)
    def test_server_error_response_hander(self):
        self.client.force_login(self.user)
        response = self.client.get('/500/')

        self.assertEqual(response.status_code, 500)
        self.assertTrue('Oops' in str(response.content))