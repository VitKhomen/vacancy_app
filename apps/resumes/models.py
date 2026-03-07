from django.db import models
from django.conf import settings
from django.utils import timezone

from apps.companies.models import Company
from apps.professions.models import Profession


class Resume(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='resumes')
    profession = models.ForeignKey(
        Profession, on_delete=models.CASCADE, related_name='resumes')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(
        max_length=20,
        choices=[
            ('male', 'Мужской'),
            ('female', 'Женский'),
            ('other', 'Другой')
        ],
        default='other'
    )
    phone = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    desired_salary = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume: {self.last_name} {self.first_name}"


class ResumeView(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='resume_views')
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name='views')
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Resume View"
        verbose_name_plural = "Resume Views"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "resume", "date"],
                name="unique_resume_view_per_day"
            )
        ]

    def __str__(self):
        return f"{self.company.name} viewed {self.resume} ({self.date})"
