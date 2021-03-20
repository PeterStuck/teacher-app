from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin, ProcessFormView
from django.views.generic.list import ListView

from base.models import LessonTopic
from base.forms import TopicSearchForm


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


class LessonTopicsView(LoginRequiredMixin, ListView, FormMixin):
    login_url = '/login'
    model = LessonTopic
    template_name = 'base/saved_teacher_topics.html'
    context_object_name = 'saved_topics'
    paginate_by = 20

    form_class = TopicSearchForm
    success_url = '/saved-topics/'

    def get_queryset(self):
        queryset = LessonTopic.objects.filter(teacher=self.request.user)
        keyword = self.get_searched_keyword()

        if keyword:
            queryset = queryset.filter(topic__contains=keyword)

        return queryset

    def get_searched_keyword(self):
        """ 'k' stands from keyword """
        try:
            keyword = self.request.GET['k']
            return keyword
        except MultiValueDictKeyError:
            pass

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = TopicSearchForm()

        return context


@login_required(login_url='/login')
@require_GET
def delete_saved_topic(request, pk):
    try:
        topic_to_delete = LessonTopic.objects.filter(teacher=request.user).get(pk=pk)
        topic_to_delete.delete()

        return HttpResponseRedirect(reverse('base:saved_topics'))
    except LessonTopic.DoesNotExist:
        return render(request, 'base/bad_topic_id.html')


@login_required(login_url='/login')
@require_GET
def end_of_work_view(request, filename=None):
    """ View to display when app ends work correctly """
    return render(request, 'base/end_of_work.html', context={'filename': filename})
