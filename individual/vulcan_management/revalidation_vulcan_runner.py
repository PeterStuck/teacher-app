from ..plain_classes.vulcan_data import VulcanIndividualLessonData
from .individual_lesson_agent import IndividualLessonAgent


class RevalidationVulcanRunner:

    def __init__(self, credentials: dict, vd: VulcanIndividualLessonData):
        self.vulcan_agent = IndividualLessonAgent(
            credentials=credentials,
            vulcan_data=vd)

    def run(self):
        self.vulcan_agent.go_to_lessons_menu()
        self.vulcan_agent.go_to_student_invidual_lessons()
        self.vulcan_agent.add_lesson()
        self.vulcan_agent.add_attendance_to_lesson()