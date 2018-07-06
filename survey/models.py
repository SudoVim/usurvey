from django.db import models

class SurveyQuestion(models.Model):
    question = models.TextField()

    def __str__(self):
        return self.question

class SurveyAnswer(models.Model):
    question = models.ForeignKey(
        'SurveyQuestion',
        related_name='answers',
        on_delete=models.CASCADE,
    )
    answer = models.TextField()

class SurveyResponse(models.Model):
    ip = models.GenericIPAddressField()
    question = models.ForeignKey(
        'SurveyQuestion',
        related_name='responses',
        on_delete=models.CASCADE,
    )
    answer = models.ForeignKey(
        'SurveyAnswer',
        related_name='responses',
        on_delete=models.CASCADE,
    )
