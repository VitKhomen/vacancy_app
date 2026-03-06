from turtle import st

from django.db import models
from django.conf import settings

from apps.vacancies.models import Vacancy
from apps.resumes.models import Resume


class Response(models.Model):
    vacancy = models.ForeignKey(
        Vacancy, on_delete=models.CASCADE, related_name='responses')
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name='responses')
    cover_letter = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=[
        ('new', 'новый'),
        ('viewed', 'просмотренный'),
        ('rejected', 'отклонённый'),
        ('accepted', 'принятый'),
    ], max_length=20, default='new')

    class Meta:
        verbose_name = "Response"
        verbose_name_plural = "Responses"
        constraints = [
            models.UniqueConstraint(
                fields=["vacancy", "resume"],
                name="unique_response_per_vacancy_resume"
            )
        ]

    def __str__(self):
        return f"Response to «{self.vacancy}» from {self.resume}"


class Invitation(models.Model):
    vacancy = models.ForeignKey(
        Vacancy, on_delete=models.CASCADE, related_name='invitations')
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name='invitations')
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=[
        ('new', 'новое'),
        ('accepted', 'принято'),
        ('rejected', 'отклонено'),
    ], max_length=20, default='new')

    class Meta:
        verbose_name = "Invitation"
        verbose_name_plural = "Invitations"
        constraints = [
            models.UniqueConstraint(
                fields=["vacancy", "resume"],
                name="unique_invitation_per_vacancy_resume"
            )
        ]

    def __str__(self):
        return f"Invitation to «{self.vacancy}» for {self.resume}"
