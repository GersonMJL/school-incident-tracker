from django.contrib import admin
from .models import Student, IncidentType, IncidentReport

admin.site.register(Student)
admin.site.register(IncidentType)
admin.site.register(IncidentReport)
