from django.contrib import admin
from .models import PollQuestion, PollChoice
from .models import Key

class KeyAdmin(admin.ModelAdmin):
    fields = ('name', 'owner')

class PollChoiceInline(admin.TabularInline):
	model = PollChoice
	fields = ('text', )
	extra = 1

class PollQuestionAdmin(admin.ModelAdmin):

	inlines = [
		PollChoiceInline,
	]

admin.site.register(Key, KeyAdmin)
admin.site.register(PollQuestion, PollQuestionAdmin)
