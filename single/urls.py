from django.urls import path

from .views import start

app_name = 'single'

urlpatterns = [
    path('start/', start, name='start'),
]