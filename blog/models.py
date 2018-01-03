from django.db import models
from django.conf import settings
from django.forms import ModelForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	is_administrator = models.BooleanField(default=False)
	is_president = models.BooleanField(default=False)
	is_in_executive_committee = models.BooleanField(default=False)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
	email = models.EmailField(blank=True)

class NewsPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.TextField('', max_length=200)

    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.text

class Key(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    is_used = models.BooleanField(default=False)
    
    def publish(self):
        self.save()

    def __str__(self):
        return self.name

class PollQuestion(models.Model):
    question_text = models.CharField(max_length=200)  
    due_date = models.DateTimeField(
            blank=True, null=True)

    def __str__(self):
        return self.question_text

class PollChoice(models.Model):
    poll_question = models.ForeignKey(PollQuestion, on_delete=models.CASCADE)
    text = models.CharField('Choice', max_length=200)
    number_of_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text

class Vote(models.Model):
    poll_choice = models.ForeignKey(PollChoice)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

