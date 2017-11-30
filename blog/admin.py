from django.contrib import admin
from .models import PollQuestion
from .models import Key

admin.site.register(PollQuestion)

class KeyAdmin(admin.ModelAdmin):
    fields = ('name','owner')

admin.site.register(Key, KeyAdmin)
