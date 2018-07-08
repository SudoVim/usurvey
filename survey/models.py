import random

from django.db import models

class SurveyQuestion(models.Model):
    question = models.TextField()

    def __str__(self):
        return self.question

    @classmethod
    def random_for_ip(cls, ip):
        """
            get a random entry for the given IP address or ``None`` if none
            remain
        """
        tries = 5
        query = models.Q(~models.Q(responses__ip=ip))
        while tries > 0:
            try:
                num = cls.objects.filter(query).count()
                if not num:
                    return None

                return cls.objects.filter(query)[random.randint(0, num-1)]

            # Detected a race condition whereby our random index does not match
            # a valid entry. Just try again.
            except IndexError:
                tries -= 1

        return None


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
