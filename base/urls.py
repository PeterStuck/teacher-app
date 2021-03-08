from django.urls import path
from .views import main_navigation_view, end_of_work_view

app_name = 'base'

urlpatterns = [
    path('menu/', main_navigation_view, name='main_nav'),
    path('eow/', end_of_work_view, name='eow')
]