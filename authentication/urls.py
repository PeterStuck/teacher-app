from django.urls import path
from .views import logout_view, LoginFormView, AccountOptionsView, change_password

app_name = 'authentication'

urlpatterns = [
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('account-options/', AccountOptionsView.as_view(), name='account-options'),
    path('change-password/', change_password, name='change-password'),
]