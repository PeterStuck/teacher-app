from django.shortcuts import render
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .utils.vulcan_management.individual_lesson_agent import IndividualLessonAgent
from .plain_classes.vulcan_data import VulcanIndividualLessonData
from .forms import IndividualLessonForm
from .models import RevalidationStudent

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
        form = IndividualLessonForm(user=request.user, data=request.POST)
        if form.is_valid():
            credentials = request.session['credentials']
            vulcan_agent = IndividualLessonAgent(credentials)

            # vulcan_agent.go_to_lessons_menu(department=DEPARTMENT)
            # vulcan_agent.go_to_student_invidual_lessons(student_name=STUDENT_NAME)
            # vulcan_agent.add_lesson(data)
        return render(request, 'individual/index.html', context={'individual_lesson_form': form})
    return render(request, 'individual/index.html', context={'individual_lesson_form': form})


@login_required(login_url="/login")
def load_revalidation_students(request):
    department_name = request.GET.get('department')
    revalidation_students = RevalidationStudent.objects.filter(department__name=department_name).filter(teacher=request.user).order_by('name')
    return render(request, 'individual/revalidation_students_dropdown.html', context={'revalidation_students': revalidation_students})



