from django.db import models
from django.conf import settings
from django.forms import ModelForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator, EmailValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
import datetime as dt
from datetime import datetime

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class User(AbstractUser):
    no_of_persons = models.PositiveSmallIntegerField(default=0, null=False)
    is_administrator = models.BooleanField(default=False)
    is_president = models.BooleanField(default=False)
    is_in_executive_committee = models.BooleanField(default=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    email = models.EmailField()
    surface_factor = models.FloatField(default=0.0, null=False, validators = [MinValueValidator(0.0), MaxValueValidator(1.0)])
    month_to_pay = models.FloatField(default=0.0, null=False, validators = [MinValueValidator(0.0)])
    payed_amount = models.FloatField(default=0.0, null=False, validators = [MinValueValidator(0.0)])
    debt = models.FloatField(default=0.0, null=False, validators = [MinValueValidator(0.0)])
    total_to_pay = models.FloatField(default=0.0, null=False, validators = [MinValueValidator(0.0)])
    index_vechi_apa_rece = models.FloatField(default=0.0, null=True, validators = [MinValueValidator(0.0)])
    index_vechi_apa_calda = models.FloatField(default=0.0, null=False, validators = [MinValueValidator(0.0)])
    index_curent_apa_rece = models.FloatField(default=0.0, null=False, validators = [MinValueValidator(0.0)])
    index_curent_apa_calda = models.FloatField(default=0.0, null=False, validators = [MinValueValidator(0.0)])

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

class ImportantDate(models.Model):
    description = models.CharField(max_length=30)
    monthly_due_date = IntegerRangeField(min_value=1, max_value=31,default=1)

    def __str__(self):
        return self.description

class CommonBill(models.Model):

    def monthdelta(date, delta):
        
        m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
        if not m: m = 12
        d = min(date.day, [31,
            29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
        return date.replace(day=d,month=m, year=y)

    date = models.DateField(default=monthdelta(datetime.now().date(), -1))
    gaze = models.FloatField(default=0, validators = [MinValueValidator(0.0)])
    incalzire_curenta = models.FloatField(default=0, validators = [MinValueValidator(0.0)])
    apa_calda = models.FloatField(default=0, validators = [MinValueValidator(0.0)])
    cons_apa_calda = models.FloatField(default=0, validators = [MinValueValidator(0.0)])
    apa_rece = models.FloatField(default=0, validators = [MinValueValidator(0.0)])
    cons_apa_rece = models.FloatField(default=0, validators = [MinValueValidator(0.0)])
    energie_electrica_parti_comune = models.FloatField(default=0, validators = [MinValueValidator(0.0)])
    intretinere_interfon = models.FloatField(default=0, validators = [MinValueValidator(0.0)])
    intretinere_lift = models.FloatField(default=0, validators = [MinValueValidator(0.0)])
    deseuri_menajere = models.FloatField(default=0, validators = [MinValueValidator(0.0)])
    intretinere_interfon = models.FloatField(default=0, validators = [MinValueValidator(0.0)])
    salarii_bloc = models.FloatField(default=0, validators = [MinValueValidator(0.0)])
    cheltuieli_neprevazute = models.FloatField(default=0, validators = [MinValueValidator(0.0)])

    def __str__(self):
        return "Monthly Bill " + str(self.date)

class OtherImportantContact(models.Model):
    description = models.CharField(max_length=30)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.description

class IntrariIntretinere(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateField()
    consum_apa_rece = models.FloatField(verbose_name="cons. apa rece [mc]", default=0.0,
        null=False, validators = [MinValueValidator(0.0)])
    apa_rece = models.FloatField(verbose_name="cost apa rece [lei]", default=0.0,
        null=False, validators = [MinValueValidator(0.0)])
    consum_apa_calda = models.FloatField(verbose_name="cons. apa calda [mc]", default=0.0,
        null=False, validators = [MinValueValidator(0.0)])
    apa_calda = models.FloatField(verbose_name="cost apa calda [lei]", default=0.0,
        null=False, validators = [MinValueValidator(0.0)])
    gaze = models.FloatField(verbose_name="cost gaze [lei]", default=0.0,
        null=False, validators = [MinValueValidator(0.0)])
    energie_parti_comune = models.FloatField(verbose_name="cost en. parti comune [lei]", default=0.0,
        null=False, validators = [MinValueValidator(0.0)])
    interfon = models.FloatField(verbose_name="cost intr. interfon[lei]", default=0.0,
        null=False, validators = [MinValueValidator(0.0)])
    deseuri_menajere = models.FloatField(verbose_name="cost deseuri menajere [lei]", default=0.0,
        null=False, validators = [MinValueValidator(0.0)])
    salarii = models.FloatField(verbose_name="salarii [lei]", default=0.0,
        null=False, validators = [MinValueValidator(0.0)])
    caldura = models.FloatField(verbose_name="cost caldura [lei]", default=0.0,
        null=False, validators = [MinValueValidator(0.0)])
    lift = models.FloatField(verbose_name="cost intr. lift [lei]", default=0.0,
        null=False, validators = [MinValueValidator(0.0)])
    cheltuieli_neprevazute = models.FloatField(verbose_name="chelt. neprev. [lei]", default=0.0,
        null=False, validators = [MinValueValidator(0.0)])
    total_luna_curenta = models.FloatField(default=0.0, null=False, validators = [MinValueValidator(0.0)])
    restante = models.FloatField(default=0.0, null=False, validators = [MinValueValidator(0.0)])
    total = models.FloatField(default=0.0, null=False, validators = [MinValueValidator(0.0)])
