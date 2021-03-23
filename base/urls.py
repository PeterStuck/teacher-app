from django.urls import path
from .views import MainNavigationView, LessonTopicsView, end_of_work_view, delete_saved_topic

app_name = 'base'

urlpatterns = [
    path('menu/', MainNavigationView.as_view(), name='main_nav'),
    path('saved-topics/', LessonTopicsView.as_view(), name='saved_topics'),
    path('delete-topic/<int:pk>/', delete_saved_topic, name='delete_topic'),
    path('eow/', end_of_work_view, name='eow'),
]