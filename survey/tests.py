from unittest import mock

from django.test import TestCase

from .models import SurveyQuestion, SurveyResponse

class TestSurveyQuestion(TestCase):

    def test_random(self):
        self.assertIs(SurveyQuestion.random_for_ip('127.0.0.1'), None)

        q1 = SurveyQuestion.objects.create(question='Q1')
        a1_1 = q1.answers.create(answer='Y')
        a1_2 = q1.answers.create(answer='N')

        self.assertEqual(SurveyQuestion.random_for_ip('127.0.0.1'), q1)

        # Answer this question
        SurveyResponse.objects.create(ip='127.0.0.1', question=q1, answer=a1_1)
        self.assertIs(SurveyQuestion.random_for_ip('127.0.0.1'), None)

        q2 = SurveyQuestion.objects.create(question='Q2')
        q2.answers.create(answer='Y2')
        q2.answers.create(answer='N2')

        # Now, we can get q2 as a random question for our IP
        self.assertEqual(SurveyQuestion.random_for_ip('127.0.0.1'), q2)

        # Test the retry mechanism.
        with mock.patch('random.randint', side_effect=[2, 2, 2, 2, 1]):
            self.assertEqual(SurveyQuestion.random_for_ip('127.0.0.2'), q2)

        # Test the retry mechanism's failsafe.
        with mock.patch('random.randint', side_effect=[2, 2, 2, 2, 2, 2]):
            self.assertIs(SurveyQuestion.random_for_ip('127.0.0.2'), None)

        # Try the first entry, then the second entry.
        with mock.patch('random.randint', side_effect=[0, 1]):
            # From a new IP, we should be able to query both.
            self.assertEqual(SurveyQuestion.random_for_ip('127.0.0.2'), q1)
            self.assertEqual(SurveyQuestion.random_for_ip('127.0.0.2'), q2)

        # Delete the first question so we can't query it anymore.
        SurveyQuestion.objects.get(pk=1).delete()
        self.assertEqual(SurveyQuestion.random_for_ip('127.0.0.1'), q2)
        self.assertEqual(SurveyQuestion.random_for_ip('127.0.0.2'), q2)
