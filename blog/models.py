from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.contrib.auth.models  import User

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

class Key(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey('auth.User')
    is_used = models.BooleanField(default=False)
    STATUS_CHOICES = (
        ('at me, using it' , 'AT ME, USING IT'),
        ('at me, not using it' , 'AT ME, NOT USING IT'),
        ('not at me' , 'NOT AT ME'),
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not at me')
    
    def publish(self):
        self.save()

    def __str__(self):
        return self.name
