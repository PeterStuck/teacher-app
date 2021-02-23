from django.test import TestCase

from filler.plain_classes.teams_data import TeamsData


class TestTeamsData(TestCase):

    def test_participants_none(self):
        with self.assertRaises(AssertionError):
            TeamsData(participants=None, actions=['Action'], dates=['Date'])

    def test_actions_none(self):
        with self.assertRaises(AssertionError):
            TeamsData(participants=['Some'], actions=None, dates=['Date'])

    def test_dates_none(self):
        with self.assertRaises(AssertionError):
            TeamsData(participants=['Some'], actions=['Action'], dates=None)
