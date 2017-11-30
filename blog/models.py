from django.db import models
from django.utils import timezone

class NewsPost(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.TextField('', max_length=200)

    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.text

class PollQuestion(models.Model):
    question_text = models.CharField(max_length=200)
    choice = models.CharField('Choice 1', max_length=200)

    def __str__(self):
        return self.question_text