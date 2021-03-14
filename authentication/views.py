from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import LoginForm
from .plain_classes.user_credentials import UserCredentials
from .utils.exceptions.bad_credentials_exception import BadCredentialsException


class LoginFormView(FormView):
    template_name = 'authentication/login.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(label_suffix='')
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('base:main_nav'))

        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        try:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            return authenticate_user(self.request, username, password)
        except BadCredentialsException:
            context = self.get_context_data()
            context['form'] = form
            return render(self.request, self.template_name, context=context)


def authenticate_user(request, username, password):
    """ Authenticates user and create user session if username and password are valid """
    user = authenticate(request, username=username, password=password)
    if user is not None:
        credentials = UserCredentials(email=user.email, password=password)
        request.session['credentials'] = credentials.__to_dict__()
        login(request, user)
        return redirect_after_login(request)
    raise BadCredentialsException


def redirect_after_login(request):
    next_page = request.POST.get('next')
    if next_page:
        return HttpResponseRedirect(request.POST.get('next'))
    else:
        return HttpResponseRedirect(reverse('base:main_nav'))


@login_required(login_url='/login')
def logout_view(request):
    """ Deletes user data from session """
    logout(request)
    return HttpResponseRedirect(reverse('authentication:login'))

