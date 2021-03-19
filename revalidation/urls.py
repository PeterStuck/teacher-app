from django.urls import path

from .views import load_revalidation_students, RevalidationLessonFormView, RevalidationSettingsView, save_revalidation_student

app_name = 'revalidation'

urlpatterns = [
    path('', RevalidationLessonFormView.as_view(), name='start'),
    path('settings/', RevalidationSettingsView.as_view(), name='settings'),
    path('save_revalidation_student/', save_revalidation_student, name='save_revalidation_student'),
    path('load_revalidation_students/', load_revalidation_students, name='load_revalidation_students')
]