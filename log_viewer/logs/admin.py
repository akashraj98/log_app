from django.contrib import admin
from logs import models
# Register your models here.

class LogDataAdmin(admin.ModelAdmin):
    list_display = ('level', 'message', 'resourceId', 'timestamp', 'traceId', 'spanId', 'commit', 'parentResourceId')
    list_filter = ('level', 'timestamp', 'traceId', 'spanId', 'commit', 'parentResourceId')
    list_per_page = 50

admin.site.register(models.LogData, LogDataAdmin)
