from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User

from .forms import RevalidationLessonForm, AddRevalidationStudentForm
from .models import RevalidationStudent
from .plain_classes.vulcan_data import RevalidationVulcanData
from .vulcan_management.revalidation_vulcan_runner import RevalidationVulcanRunner
from base.utils.spared_time_counter import add_spared_time_to_total
from base.models import LessonTopic, LessonCategory


class IndividualLessonFormView(LoginRequiredMixin, FormView):
    """ Main control panel to set parameters for RevalidationVulcanData and run sequence """
    login_url = "/login"

    template_name = 'revalidation/index.html'
    form_class = RevalidationLessonForm
    success_url = '/eow/'
    initial = {
        'date': datetime.now().strftime('%d.%m.%Y'),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['revalidation_lesson_form'] = self.form_class(
            user=self.request.user,
            label_suffix='',
            initial=self.get_initial())
        return context

    def get_form(self, form_class=None):
        return self.form_class(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        logged_user = self.request.user
        save_revalidation_topic(form=form, logged_user=logged_user)

        credentials = self.request.session['credentials']
        vd: RevalidationVulcanData = form.parse_to_vulcan_data()

        runner = RevalidationVulcanRunner(credentials=credentials, vd=vd)
        spared_time = runner.run()
        add_spared_time_to_total(spared_time, user=logged_user)

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['revalidation_lesson_form'] = form
        context['revalidation_lesson_form'].label_suffix = ''
        return self.render_to_response(context)


def save_revalidation_topic(form: RevalidationLessonForm, logged_user: User):
    """ Exception means that given topic wasn't found in associated user's topics. """
    try:
        topic = form['topic'].data.title()
        if LessonTopic.objects.filter(teacher=logged_user).get(topic__exact=topic):
            return None
    except Exception as e:
        revalidation_category = LessonCategory.objects.get(name__exact='rewalidacja'.title())
        LessonTopic.objects.create(
            topic=topic,
            is_individual=True,
            teacher=logged_user,
            category=revalidation_category
        )


class RevalidationSettingsView(LoginRequiredMixin, TemplateView):
    login_url = '/login'
    template_name = 'revalidation/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_revalidation_student_form'] = AddRevalidationStudentForm(
            user=self.request.user,
            label_suffix='')

        return context


@login_required(login_url='/login')
def save_revalidation_student(request):
    if request.method == "POST":
        rsf = AddRevalidationStudentForm(user=request.user, data=request.POST)
        if rsf.is_valid():
            rsf.save(commit=True)
            return redirect(reverse('revalidation:settings') + "?status=1")
        return redirect(reverse('revalidation:settings') + "?status=0")


@login_required(login_url="/login")
def load_revalidation_students(request):
    department_name = request.GET.get('department')
    revalidation_students = RevalidationStudent.objects.filter(department__name=department_name).filter(teacher=request.user).order_by('name')
    return render(request, 'revalidation/revalidation_students_dropdown.html', context={'revalidation_students': revalidation_students})



