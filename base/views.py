from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from base.models import LessonTopic


class MainNavigationView(LoginRequiredMixin, TemplateView):
    login_url = '/login'
    template_name = 'base/main_nav.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spared_time = get_user_spared_time(self.request.user)
        context['spared_time'] = spared_time
        context['has_spared_time'] = (spared_time._has_time == 1)

        return context


def get_user_spared_time(user):
    """ Returns User object with access to particular time units """
    if not hasattr(user, 'sparedtime'):
        raise AttributeError("User has no SparedTime object associated.")
    spared_time_in_sec = user.sparedtime.time
    return relativedelta(seconds=spared_time_in_sec)


class LessonTopicsView(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = LessonTopic
    template_name = 'base/saved_teacher_topics.html'
    context_object_name = 'saved_topics'
    paginate_by = 20

    def get_queryset(self):
        return LessonTopic.objects.filter(teacher=self.request.user)


@login_required(login_url='/login')
def delete_saved_topic(request, pk):
    try:
        topic_to_delete = LessonTopic.objects.filter(teacher=request.user).get(pk=pk)
        topic_to_delete.delete()

        return HttpResponseRedirect(reverse('base:saved_topics'))
    except LessonTopic.DoesNotExist:
        return render(request, 'base/bad_topic_id.html', {})


@login_required(login_url='/login')
def end_of_work_view(request, filename=None):
    """ View to display when filler ends work correctly """
    return render(request, 'base/end_of_work.html', context={'filename': filename})
