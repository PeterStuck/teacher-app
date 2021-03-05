from django.urls import path
from .views import main_navigation_view

app_name = 'base'

urlpatterns = [
    path('menu/', main_navigation_view, name='main_nav'),
]