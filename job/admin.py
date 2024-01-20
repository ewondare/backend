from django.contrib import admin
from .models import Industry, Job, ApplyJob

admin.site.register(Industry)
admin.site.register(ApplyJob)
admin.site.register(Job)