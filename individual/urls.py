from django.urls import path

from .views import start, load_revalidation_students

app_name = 'individual'

urlpatterns = [
    path('', start, name='start'),
    path('load_revalidation_students/', load_revalidation_students, name='load_revalidation_students')
]