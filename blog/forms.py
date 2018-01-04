from django import forms
from .models import NewsPost
from .models import Key
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))

class NewsPostForm(forms.ModelForm):

    class Meta:
        model = NewsPost
        fields = ('text',)

    def __init__(self, *args, **kwargs):          
        super(NewsPostForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = u'Add your post here...'
        self.fields['text'].widget.attrs['rows'] = 1
