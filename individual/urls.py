from django.urls import path

from .views import load_revalidation_students, IndividualLessonFormView

app_name = 'individual'

urlpatterns = [
    path('', IndividualLessonFormView.as_view(), name='start'),
    path('load_revalidation_students/', load_revalidation_students, name='load_revalidation_students')
]