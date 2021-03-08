from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import IndividualLessonForm
from .models import RevalidationStudent
from .plain_classes.vulcan_data import VulcanIndividualLessonData
from .utils.vulcan_management.individual_lesson_agent import IndividualLessonAgent

DEPARTMENT = 'SPBrza'
STUDENT_NAME = 'Tomek'

data = VulcanIndividualLessonData(
    department=DEPARTMENT,
    date=datetime.now(),
    topic='Some topic',
    comments='Some comments',
    payment_type='W ramach pensum',
    num_of_hours=1,
    presency_status='obecny'
)


@login_required(login_url='/login')
def start(request):
    form = IndividualLessonForm(user=request.user, label_suffix='', initial={'date': datetime.now().strftime('%d.%m.%Y')})
    if request.method == 'POST':
        form = IndividualLessonForm(request.user, request.POST, label_suffix='')
        if form.is_valid():
            credentials = request.session['credentials']
            vulcan_agent = IndividualLessonAgent(credentials)

            # vulcan_agent.go_to_lessons_menu(department=DEPARTMENT)
            # vulcan_agent.go_to_student_invidual_lessons(student_name=STUDENT_NAME)
            # vulcan_agent.add_lesson(data)
        print(form.errors)
        return render(request, 'individual/index.html', context={'individual_lesson_form': form})
    return render(request, 'individual/index.html', context={'individual_lesson_form': form})


@login_required(login_url="/login")
def load_revalidation_students(request):
    department_name = request.GET.get('department')
    revalidation_students = RevalidationStudent.objects.filter(department__name=department_name).filter(teacher=request.user).order_by('name')
    return render(request, 'individual/revalidation_students_dropdown.html', context={'revalidation_students': revalidation_students})



