from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


class SchoolAdmin(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="school_admin_profile"
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
