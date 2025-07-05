from django.contrib import admin

from .models import IncidentReport, IncidentType, Student

admin.site.register(Student)
admin.site.register(IncidentType)
admin.site.register(IncidentReport)
