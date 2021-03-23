from datetime import datetime as dt

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.debug import sensitive_post_parameters, sensitive_variables

from base.utils.spared_time_counter import add_spared_time_to_total
from filler.vulcan_management.filler_vulcan_runner import FillerVulcanRunner
from wku_django.settings import BASE_DIR
from .attendance_manager.settings import files_settings, webdriver_settings
from .forms import FillerForm, ArchiveSettingsForm, WebdriverSettingsForm
from .plain_classes.vulcan_data import FillerVulcanData
from .utils.override_file_storage import OverrideFileStorage


class FillerFormView(LoginRequiredMixin, FormView):
    login_url = '/login'

    template_name = 'filler/index.html'
    form_class = FillerForm
    success_url = '/eow/'
    initial = {
        'date': str(dt.now().strftime('%Y-%m-%d')),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filler_form'] = self.form_class(
            label_suffix='',
            initial=self.get_initial())

        return context

    @sensitive_variables('request')
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    @sensitive_variables()
    def form_valid(self, form):
        credentials = self.request.session['credentials']
        vd: FillerVulcanData = form.parse_to_vulcan_data()
        if not vd.file_not_loaded and vd.teams_file is not None:
            save_file(vd.filename, vd.teams_file)

        runner = FillerVulcanRunner(credentials=credentials, vulcan_data=vd)

        spared_time = runner.run()
        add_spared_time_to_total(time_in_sec=spared_time, user=self.request.user)

        return redirect(self.get_success_url(), filename=vd.filename)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['filler_form'] = form
        context['filler_form'].label_suffix = ''

        return self.render_to_response(context)


def save_file(filename: str, file):
    fs = OverrideFileStorage()
    fs.save(f'teams/{filename}', file)


class SettingsView(LoginRequiredMixin, TemplateView):
    login_url = '/login'
    template_name = 'filler/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['archive_form'] = self.prepopulate_archive_form()
        context['webdriver_form'] = self.prepopulate_webdriver_form()

        return context

    def prepopulate_archive_form(self):
        settings = files_settings.FilesSettings().load_settings()
        return ArchiveSettingsForm(
            label_suffix='',
            initial={'archive_desktop_path': BASE_DIR / settings['archive_desktop_path']})

    def prepopulate_webdriver_form(self):
        settings = webdriver_settings.WebdriverSettings().load_settings()
        return WebdriverSettingsForm(
            label_suffix='',
            initial={'vulcan_url': settings['vulcan_url']})


@login_required(login_url='/login')
@require_POST
def update_file_settings(request):
    form = ArchiveSettingsForm(request.POST)
    if form.is_valid():
        new_archive_path = form.cleaned_data['archive_desktop_path']
        settings = files_settings.FilesSettings()
        settings_data = settings.load_settings()
        settings_data['archive_desktop_path'] = new_archive_path
        settings.update_settings(settings_data)
        return HttpResponseRedirect('/filler/settings?status=1')
    return HttpResponseRedirect('/filler/settings?status=0')


@login_required(login_url='/login')
@require_POST
def update_webdriver_settings(request):
    form = WebdriverSettingsForm(request.POST)
    if form.is_valid():
        new_vulcan_url = form.cleaned_data['vulcan_url']

        settings = webdriver_settings.WebdriverSettings()
        settings_data = settings.load_settings()
        settings_data['vulcan_url'] = new_vulcan_url
        settings.update_settings(settings_data)
        return HttpResponseRedirect('/filler/settings?status=1')
    return HttpResponseRedirect('/filler/settings?status=0')
