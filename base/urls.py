from django.urls import path
from .views import MainNavigationView, end_of_work_view

app_name = 'base'

urlpatterns = [
    path('menu/', MainNavigationView.as_view(), name='main_nav'),
    path('eow/', end_of_work_view, name='eow')
]