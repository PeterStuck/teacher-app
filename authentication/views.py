from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.contrib.auth.models import User

from .forms import LoginForm, ChangePasswordForm
from .plain_classes.user_credentials import UserCredentials
from .utils.exceptions.bad_credentials_exception import BadCredentialsException


class LoginFormView(FormView):
    template_name = 'authentication/login.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = self.form_class(label_suffix='')

        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('base:main_nav'))

        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        try:
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            return authenticate_user(self.request, email, password)
        except BadCredentialsException:
            context = self.get_context_data()
            context['login_form'] = form
            return render(self.request, self.template_name, context=context)


def authenticate_user(request, email, password):
    """ Authenticates user and create user session if username and password are valid """
    user_with_given_email: User = User.objects.filter(email=email).first()

    if user_with_given_email is None:
        raise BadCredentialsException

    user = authenticate(request, username=user_with_given_email.username, password=password)
    if user is not None:
        credentials = UserCredentials(email=user.email, password=password)
        request.session['credentials'] = credentials.__to_dict__()
        login(request, user)
        return redirect_after_login(request.POST.get('next'))
    raise BadCredentialsException


def redirect_after_login(next_page):
    if next_page:
        return HttpResponseRedirect(next_page)
    else:
        return HttpResponseRedirect(reverse('base:main_nav'))


class AccountOptionsView(LoginRequiredMixin, TemplateView):
    login_url = '/login'
    template_name = 'authentication/account_options.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['change_password_form'] = ChangePasswordForm(label_suffix='')

        return context


@login_required(login_url='/login')
@require_POST
def change_password(request):
    logged_user = request.user
    form = ChangePasswordForm(request.POST)
    if form.is_valid():
        old_pass = form.cleaned_data['old_password']
        new_pass = form.cleaned_data['new_password']
        if logged_user.check_password(old_pass):
            logged_user.set_password(new_pass)
            logged_user.save()
            return HttpResponseRedirect('/account-options?status=1')
    return HttpResponseRedirect('/account-options?status=0')


@login_required(login_url='/login')
@require_GET
def logout_view(request):
    """ Deletes user data from session """
    logout(request)
    return HttpResponseRedirect(reverse('authentication:login'))

