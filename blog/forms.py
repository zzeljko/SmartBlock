from django import forms

from .models import NewsPost

class NewsPostForm(forms.ModelForm):

    class Meta:
        model = NewsPost
        fields = ('text',)

    def __init__(self, *args, **kwargs):          
        super(NewsPostForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = u'Add your post here...'
        self.fields['text'].widget.attrs['rows'] = 4