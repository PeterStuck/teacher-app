from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta


@login_required(login_url='/login')
def main_navigation_view(request):
    spared_time = get_user_spared_time(request.user)
    context = {
        'spared_time': spared_time,
        'has_spared_time': (spared_time._has_time == 1)
    }
    return render(request, 'base/main_nav.html', context=context)


def get_user_spared_time(user):
    """ Returns object with access to particular time units """
    if not hasattr(user, 'sparedtime'):
        raise AttributeError("User has no SparedTime object associated.")
    spared_time_in_sec = user.sparedtime.time
    return relativedelta(seconds=spared_time_in_sec)


@login_required(login_url='/login')
def end_of_work_view(request, filename=None):
    """ View to display when filler ends work correctly """
    return render(request, 'base/end_of_work.html', context={'filename': filename})
