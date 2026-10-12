from django.conf import settings
from django.db import models


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
    )
    full_name = models.CharField(max_length=150)
    faculty_id = models.CharField(max_length=30, unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    cabin = models.CharField(max_length=150)
    call_hours = models.CharField(max_length=150)
    subjects = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.full_name} ({self.faculty_id})"