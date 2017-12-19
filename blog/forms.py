from django import forms
from .models import NewsPost
from .models import Key

class NewsPostForm(forms.ModelForm):

    class Meta:
        model = NewsPost
        fields = ('text',)

    def __init__(self, *args, **kwargs):          
        super(NewsPostForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = u'Add your post here...'
        self.fields['text'].widget.attrs['rows'] = 1


# class KeyForm(forms.ModelForm):

# 	class Meta:
# 		model = Key
# 		fields = ('name','status',)
