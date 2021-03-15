from django.urls import path
from .views import start, settings_view, update_file_settings, update_webdriver_settings

app_name = 'filler'
urlpatterns = [
    path('', start, name='filler_start'),
    path('settings/', settings_view, name='settings'),
    path('settings/update_files/', update_file_settings, name='update_file_settings'),
    path('settings/update_webdriver/', update_webdriver_settings, name='update_webdriver_settings'),
]