from django.test import TestCase
from .plain_classes.vulcan_data import VulcanIndividualLessonData


class VulcanIndividualLessonDataTest(TestCase):
    def setUp(self):
        self.vulcan_data = None

    def test_department_not_none(self):
        with self.assertRaises(AssertionError):
            self.vulcan_data = VulcanIndividualLessonData(department=None)

    def test_date_not_none(self):
        with self.assertRaises(AssertionError):
            self.vulcan_data = VulcanIndividualLessonData(date=None)

    def test_topic_not_none(self):
        with self.assertRaises(AssertionError):
            self.vulcan_data = VulcanIndividualLessonData(topic=None)

    def test_payment_type_not_none(self):
        with self.assertRaises(AssertionError):
            self.vulcan_data = VulcanIndividualLessonData(payment_type=None)

    def test_num_of_hours_not_none(self):
        with self.assertRaises(AssertionError):
            self.vulcan_data = VulcanIndividualLessonData(num_of_hours=None)

    def test_presency_status_not_none(self):
        with self.assertRaises(AssertionError):
            self.vulcan_data = VulcanIndividualLessonData(presency_status=None)