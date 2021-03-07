from django.shortcuts import render
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

from .utils.vulcan_management.individual_lesson_agent import IndividualLessonAgent
from .plain_classes.vulcan_data import VulcanIndividualLessonData

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
    if request.method == 'POST':
        credentials = request.session['credentials']
        vulcan_agent = IndividualLessonAgent(credentials)

        vulcan_agent.go_to_lessons_menu(department=DEPARTMENT)
        vulcan_agent.go_to_student_invidual_lessons(student_name=STUDENT_NAME)
        vulcan_agent.add_lesson(data)

    return render(request, 'individual/index.html', context={})



