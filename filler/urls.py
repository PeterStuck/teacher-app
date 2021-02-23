from django.urls import path
from .views import filler_form_view, settings_view, update_file_settings, update_webdriver_settings, update_credentials, end_of_work_view

app_name = 'filler'
urlpatterns = [
    path('', filler_form_view, name='filler_start'),
    path('settings/', settings_view, name='settings'),
    path('settings/update_files/', update_file_settings, name='update_file_settings'),
    path('settings/update_webdriver/', update_webdriver_settings, name='update_webdriver_settings'),
    path('settings/update_credentials/', update_credentials, name='update_credentials'),
    path('eow/', end_of_work_view, name='eow'),
]