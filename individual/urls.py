from django.urls import path

from .views import start

app_name = 'individual'

urlpatterns = [
    path('', start, name='start'),
]