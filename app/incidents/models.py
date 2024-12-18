from django.db import models
from users.models import SchoolAdmin


class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    parent_email = models.EmailField(null=True, blank=True)
    school_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name} ({self.school_id})"


class IncidentType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class IncidentReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    incident_type = models.ForeignKey(
        IncidentType, on_delete=models.SET_NULL, null=True
    )
    description = models.TextField()
    pdf_file = models.CharField(
        max_length=255, null=True, blank=True
    )  # URL to PDF file
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(SchoolAdmin, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Incident for {self.student.name} - {self.incident_type.name}"
