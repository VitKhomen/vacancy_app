from django.db import models
from django.conf import settings

from .utils import company_logos_upload_path
from apps.accounts.utils import validate_avatar_size


class Company(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='company')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(
        upload_to=company_logos_upload_path,
        blank=True,
        null=True,
        validators=[validate_avatar_size])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        feedback = self.feedbacks.all()
        if feedback.exists():
            return round(sum(f.rating for f in feedback) / feedback.count(), 1)
        return 0


class FeedbackCompany(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='feedbacks')
    comment = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Отзыв о {self.company.name} — {self.rating}/5"


class FavoriteVacancy(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_vacancies')
    vacancy = models.ForeignKey(
        "vacancies.Vacancy", on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Favorite Vacancy"
        verbose_name_plural = "Favorite Vacancies"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "vacancy"],
                name="unique_favorite_vacancy"
            )
        ]

    def __str__(self):
        return f"Favorite Vacancy: {self.vacancy} by {self.user}"
