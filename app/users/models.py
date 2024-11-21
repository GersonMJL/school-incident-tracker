from django.contrib.auth.models import AbstractUser
from django.db import models


class AdminUser(AbstractUser):
    is_email_verified = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.username
