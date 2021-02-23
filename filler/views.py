from django.shortcuts import render, reverse, HttpResponseRedirect

from .forms import FillerStartForm, ArchiveSettingsForm, WebdriverSettingsForm, ChangeCredentialsForm
from .plain_classes.vulcan_data import VulcanData
from filler.attendance_manager.vulcan_management.vulcan_runner import VulcanAttendanceFiller
from .utils.override_file_storage import OverrideFileStorage
from .attendance_manager.settings import files_settings, webdriver_settings
from filler.attendance_manager.credentials_management.credentials_updater import CredentialsUpdater

from datetime import datetime as dt


def filler_form_view(request):
    """ Main control panel to set parameters for VulcanAttendaceFiller """
    form = FillerStartForm(label_suffix='', initial={'date': dt.now().strftime('%Y-%m-%d')})
    if request.method == 'POST':
        form = FillerStartForm(request.POST, request.FILES, label_suffix='')
        if form.is_valid():
            file = form.cleaned_data['file']
            file_not_loaded = form.cleaned_data['file_not_loaded']
            department = form.cleaned_data['departments']
            day = form.cleaned_data['day']
            date = form.cleaned_data['date'].strftime('%Y-%m-%d')
            lesson = form.cleaned_data['lesson_number']
            is_double_lesson = form.cleaned_data['is_double_lesson']
            absent_symbol = form.cleaned_data['absent_symbol']

            filename = None

            if not file_not_loaded and file is not None:
                filename = str(date) + '-' + department + '-' + lesson
                save_file(filename, file)
            elif not file_not_loaded and file is None:
                error_message = 'Musisz wgrać plik lub wybrać opcję poniżej zaznaczając kwadracik, aby program mógł przystąpić do działania.'
                return render(request, 'filler/filler_start_form.html', {
                    'form': form,
                    'error_message': error_message
                })

            vulcan_data = VulcanData(file=file, file_not_loaded=file_not_loaded, department=department, day=day, date=date, lesson=lesson, absent_symbol=absent_symbol)
            vulcan_runner = VulcanAttendanceFiller(data=vulcan_data, is_double_lesson=is_double_lesson)
            vulcan_runner.start_sequence()

            return render(request, 'filler/eow.html', context={'filename': filename})
    return render(request, 'filler/filler_start_form.html', context={'form': form})


def save_file(filename: str, file):
    fs = OverrideFileStorage()
    fs.save(f'teams/{filename}.csv', file)


def settings_view(request):
    credentials_form = ChangeCredentialsForm(label_suffix='')
    archive_form = prepopulate_archive_form()
    webdriver_form = prepopulate_webdriver_form()

    context = {
        'archive_form': archive_form,
        'credentials_form': credentials_form,
        'webdriver_form': webdriver_form,
    }

    return render(request, 'filler/settings.html', context=context)


def prepopulate_archive_form():
    settings = files_settings.FilesSettings()
    settings_dict = settings.load_settings()
    return ArchiveSettingsForm(label_suffix='', initial={'path': settings_dict['archive_desktop_path'],})


def prepopulate_webdriver_form():
    settings = webdriver_settings.WebdriverSettings()
    settings_dict = settings.load_settings()
    return WebdriverSettingsForm(label_suffix='', initial={'path': settings_dict['path'], 'vulcan_url': settings_dict['vulcan_url']})


def update_file_settings(request):
    if request.method == "POST":
        form = ArchiveSettingsForm(request.POST)
        if form.is_valid():
            new_archive_path = form.cleaned_data['path']
            settings = files_settings.FilesSettings()
            settings_data = settings.load_settings()
            settings_data['archive_desktop_path'] = new_archive_path
            settings.update_settings(settings_data)

    return HttpResponseRedirect(reverse('filler:settings'))


def update_webdriver_settings(request):
    if request.method == "POST":
        form = WebdriverSettingsForm(request.POST)
        if form.is_valid():
            new_path = form.cleaned_data['path']
            new_vulcan_url = form.cleaned_data['vulcan_url']

            settings = webdriver_settings.WebdriverSettings()
            settings_data = settings.load_settings()
            settings_data['path'] = new_path
            settings_data['vulcan_url'] = new_vulcan_url
            settings.update_settings(settings_data)

    return HttpResponseRedirect(reverse('filler:settings'))


def update_credentials(request):
    if request.method == "POST":
        form = ChangeCredentialsForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['email']
            new_pass = form.cleaned_data['passw']
            credentials_updater = CredentialsUpdater()
            credentials_updater.update_credentials(plain_email=new_email, plain_pass=new_pass)

    return HttpResponseRedirect(reverse('filler:settings'))


def end_of_work_view(request, filename=None):
    return render(request, 'filler/eow.html', context={'filename': filename})
