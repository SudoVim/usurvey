from unittest import mock

from django.test import TestCase

from .models import SurveyQuestion

class TestSurveyQuestion(TestCase):

    def test_random(self):
        q1 = SurveyQuestion.objects.create(question='Q1')
        q1.answers.create(answer='Y')
        q1.answers.create(answer='N')

        self.assertEqual(SurveyQuestion.random(), q1)

        q2 = SurveyQuestion.objects.create(question='Q2')
        q2.answers.create(answer='Y2')
        q2.answers.create(answer='N2')

        # Delete the first question so we can get a key mismatch on random.
        SurveyQuestion.objects.get(pk=1).delete()

        # Try the deleted entry then the existing entry. This tests the
        # DoesNotExist branch.
        with mock.patch('random.randint', side_effect=[1, 2]):
            self.assertEqual(SurveyQuestion.random(), q2)
