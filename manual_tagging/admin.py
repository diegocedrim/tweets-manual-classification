from django.contrib import admin
from .models import *


class TweetTagAdmin(admin.ModelAdmin):
    readonly_fields = ('tweet', 'user', 'last_update')
    list_filter = ('user', 'last_update', 'classification')
    list_display = ('tweet', 'classification', 'last_update', 'user')

# Register your models here.
admin.site.register(TweetDataset)
admin.site.register(TweetClassification)
admin.site.register(Tweet)
admin.site.register(TweetTag, TweetTagAdmin)
