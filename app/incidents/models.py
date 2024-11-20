from django.db import models


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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Incident for {self.student.name} - {self.incident_type.name}"
