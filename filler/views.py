from datetime import datetime as dt

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect

from filler.attendance_manager.vulcan_runner import VulcanAttendanceFiller
from base.utils.spared_time_counter import add_spared_time_to_total
from wku_django.settings import BASE_DIR
from .attendance_manager.settings import files_settings, webdriver_settings
from .forms import FillerStartForm, ArchiveSettingsForm, WebdriverSettingsForm, ChangePasswordForm
from .plain_classes.vulcan_data import VulcanData
from .utils.override_file_storage import OverrideFileStorage


@login_required(login_url='/login')
def start(request):
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
                return render(request, 'filler/index.html', {
                    'form': form,
                    'error_message': error_message
                })

            vulcan_data = VulcanData(file=file, file_not_loaded=file_not_loaded, department=department, day=day, date=date, lesson=lesson, absent_symbol=absent_symbol)
            vulcan_runner = VulcanAttendanceFiller(data=vulcan_data, is_double_lesson=is_double_lesson, credentials=request.session['credentials'])
            spared_time = vulcan_runner.start_sequence()
            add_spared_time_to_total(time_in_sec=spared_time, user=request.user)

            return render(request, 'base/end_of_work.html', context={'filename': filename})
    return render(request, 'filler/index.html', context={'form': form})


def save_file(filename: str, file):
    fs = OverrideFileStorage()
    fs.save(f'teams/{filename}.csv', file)


@login_required(login_url='/login')
def settings_view(request):
    credentials_form = ChangePasswordForm(label_suffix='')
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
    return ArchiveSettingsForm(label_suffix='', initial={'path': BASE_DIR / settings_dict['archive_desktop_path'],})


def prepopulate_webdriver_form():
    settings = webdriver_settings.WebdriverSettings()
    settings_dict = settings.load_settings()
    return WebdriverSettingsForm(label_suffix='', initial={'path': settings_dict['path'], 'vulcan_url': settings_dict['vulcan_url']})


@login_required(login_url='/login')
def update_file_settings(request):
    if request.method == "POST":
        form = ArchiveSettingsForm(request.POST)
        if form.is_valid():
            new_archive_path = form.cleaned_data['path']
            settings = files_settings.FilesSettings()
            settings_data = settings.load_settings()
            settings_data['archive_desktop_path'] = new_archive_path
            settings.update_settings(settings_data)
            return HttpResponseRedirect('/filler/settings?status=1')
        return HttpResponseRedirect('/filler/settings?status=0')


@login_required(login_url='/login')
def update_webdriver_settings(request):
    if request.method == "POST":
        form = WebdriverSettingsForm(request.POST)
        if form.is_valid():
            new_vulcan_url = form.cleaned_data['vulcan_url']

            settings = webdriver_settings.WebdriverSettings()
            settings_data = settings.load_settings()
            settings_data['vulcan_url'] = new_vulcan_url
            settings.update_settings(settings_data)
            return HttpResponseRedirect('/filler/settings?status=1')
        return HttpResponseRedirect('/filler/settings?status=0')


@login_required(login_url='/login')
def update_credentials(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_pass = form.cleaned_data['old_passw']
            new_pass = form.cleaned_data['passw']
            if request.user.check_password(old_pass):
                user = request.user
                user.set_password(new_pass)
                user.save()
                return HttpResponseRedirect('/filler/settings?status=1')
        return HttpResponseRedirect('/filler/settings?status=0')
