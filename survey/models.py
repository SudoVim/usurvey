import random

from django.db import models

class SurveyQuestion(models.Model):
    question = models.TextField()

    def __str__(self):
        return self.question

    @classmethod
    def random(cls):
        """
            get a random entry
        """
        max_pk = cls.objects.values_list('pk', flat=True).order_by('-pk')[0]
        while True:
            try:
                return cls.objects.get(pk=random.randint(1, max_pk))

            except cls.DoesNotExist:
                pass

class SurveyAnswer(models.Model):
    question = models.ForeignKey(
        'SurveyQuestion',
        related_name='answers',
        on_delete=models.CASCADE,
    )
    answer = models.TextField()

    def __str__(self):
        return self.answer

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

    class Meta:
        unique_together = (('ip', 'question'),)
