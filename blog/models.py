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

class PollQuestion(models.Model):
    question_text = models.CharField(max_length=200)
    choice = models.CharField('Choice 1', max_length=200)

    def __str__(self):
        return self.question_text

class Key(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    is_used = models.BooleanField(default=False)
    
    def publish(self):
        self.save()

    def __str__(self):
        return self.name

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     is_administrator = models.NullBooleanField(default=False)
#     is_president = models.NullBooleanField(default=False)
#     is_in_executive_committee = models.NullBooleanField(default=False)
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
#     phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
#     email = models.EmailField(blank=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

