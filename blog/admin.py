from django.contrib import admin
from .models import Post, Key

admin.site.register(Post)

class KeyAdmin(admin.ModelAdmin):
    fields = ('name','owner')

admin.site.register(Key, KeyAdmin)
