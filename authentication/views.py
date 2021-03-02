from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm
from .plain_classes.user_credentials import UserCredentials


def login_view(request):
    """ Start place for all applications in this webapp.
        To enter any app user needs to be authenticated first."""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('filler:filler_start'))

    login_form = LoginForm(label_suffix='')
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            next_page = request.POST.get('next')
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            if authenticate_user(request, username, password):
                if next_page:
                    return HttpResponseRedirect(request.POST.get('next'))
                else:
                    return HttpResponseRedirect(reverse('filler:filler_start'))
    return render(request, 'authentication/login.html', context={'form': login_form})


def authenticate_user(request, username, password):
    """ Authenticates user and create user session if username and password are valid """
    user = authenticate(request, username=username, password=password)
    if user is not None:
        credentials = UserCredentials(email=user.email, password=password)
        request.session['credentials'] = credentials.__to_dict__()
        login(request, user)
    return user is not None


def logout_view(request):
    """ Deletes user data from session """
    logout(request)
    return HttpResponseRedirect(reverse('authentication:login'))

