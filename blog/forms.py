from django import forms
from .models import Post, Key

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class KeyForm(forms.ModelForm):

	class Meta:
		model = Key
		fields = ('fuckYOU', 'name','owner',)