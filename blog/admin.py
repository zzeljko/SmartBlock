from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import PollQuestion, PollChoice
from .models import Key, User, ImportantDate, OtherImportantContact, CommonBill
from .widgets import MonthYearWidget

class UserCreationFormExtended(UserCreationForm):
	"""A form for creating new users. Includes all the required
	fields, plus a repeated password."""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
        	user.save()
        return user

class UserChangeFormExtended(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super(UserChangeFormExtended, self).__init__(*args, **kwargs)

class CustomUserAdmin(UserAdmin):
	model = User
	list_display = UserAdmin.list_display + ('phone_number', 'is_president', 'is_in_executive_committee', 'is_administrator',)
	add_form = UserCreationFormExtended
	form = UserChangeFormExtended
	add_fieldsets = (
    	(None, {
        	'classes': ('wide',),
        	'fields': ('username', 'password1', 'password2', 'no_of_persons', 'surface_factor', 'payed_amount', 'phone_number', 'email', 'is_president', 'is_in_executive_committee', 'is_administrator', )
    	}),
    	)
        fieldsets = (
                    (None, {
                        'fields': ('no_of_persons', 'surface_factor', 'payed_amount', 'phone_number', 'is_president', 'is_in_executive_committee', 'is_administrator', )
                    }),
                ) + UserAdmin.fieldsets

class KeyAdmin(admin.ModelAdmin):
	fields = ('name','owner')

class PollChoiceInline(admin.TabularInline):
	model = PollChoice
	fields = ('text', )
	extra = 1

class PollQuestionAdmin(admin.ModelAdmin):

	inlines = [
		PollChoiceInline,
	]

admin.site.register(User, CustomUserAdmin)
admin.site.register(Key, KeyAdmin)
admin.site.register(PollQuestion, PollQuestionAdmin)
admin.site.register(ImportantDate)
admin.site.register(OtherImportantContact)
admin.site.register(CommonBill)