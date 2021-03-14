from django.urls import path
from .views import logout_view, LoginFormView

app_name = 'authentication'

urlpatterns = [
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', logout_view, name='logout')
]