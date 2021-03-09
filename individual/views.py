from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import IndividualLessonForm
from .models import RevalidationStudent
from .plain_classes.vulcan_data import VulcanIndividualLessonData
from individual.vulcan_management.individual_lesson_agent import IndividualLessonAgent
from individual.vulcan_management.revalidation_vulcan_runner import RevalidationVulcanRunner

DEPARTMENT = 'SPBrza'
STUDENT_NAME = 'Tomek'

data = VulcanIndividualLessonData(
    department=DEPARTMENT,
    date=datetime.now(),
    topic='Some topic',
    comments='Some comments',
    payment_type='W ramach pensum',
    num_of_hours=1,
    presence_symbol='obecny'
)


class IndividualLessonFormView(LoginRequiredMixin, FormView):
    login_url = "/login"

    template_name = 'individual/index.html'
    form_class = IndividualLessonForm
    success_url = '/eow/'
    initial = {
        'date': datetime.now().strftime('%d.%m.%Y'),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['individual_lesson_form'] = self.form_class(
            user=self.request.user,
            label_suffix='',
            initial=self.get_initial())
        return context

    def get_form(self, form_class=None):
        return self.form_class(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        credentials = self.request.session['credentials']
        vd: VulcanIndividualLessonData = form.parse_to_vulcan_data()

        runner = RevalidationVulcanRunner(credentials=credentials, vd=vd)
        runner.run()

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['individual_lesson_form'] = form
        context['individual_lesson_form'].label_suffix = ''
        return self.render_to_response(context)


@login_required(login_url="/login")
def load_revalidation_students(request):
    department_name = request.GET.get('department')
    revalidation_students = RevalidationStudent.objects.filter(department__name=department_name).filter(teacher=request.user).order_by('name')
    return render(request, 'individual/revalidation_students_dropdown.html', context={'revalidation_students': revalidation_students})



