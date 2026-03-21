from django.db import models
from django.conf import settings

from apps.professions.models import Profession


class VacancyQuerySet(models.QuerySet):
    def visible_for_user(self, user):
        if not user.is_authenticated:
            return self

        # IDs of vacancies hidden by the user
        hidden_vacancies = user.hidden_vacancies.values_list(
            'vacancy_id', flat=True
        )

        # IDs of companies hidden by the user
        hidden_companies = user.hidden_companies.values_list(
            'company_id', flat=True
        )

        return self.exclude(
            id__in=hidden_vacancies
        ).exclude(
            company_id__in=hidden_companies
        )


class Vacancy(models.Model):
    objects = VacancyQuerySet.as_manager()

    company = models.ForeignKey(
        "companies.Company", on_delete=models.CASCADE, related_name='vacancies')
    profession = models.ForeignKey(
        Profession, on_delete=models.CASCADE, related_name='vacancies')
    title = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    salary = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    salary_from = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    salary_to = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    salary_type = models.CharField(
        max_length=50,
        choices=[
            ('weekly', 'раз в неделю'),
            ('monthly', 'раз в месяц'),
            ('twice_monthly', '2 раза в месяц'),
            ('daily', 'ежедневно'),
            ('hourly', 'по часам'),
            ('negotiated', 'договорная'),
        ],
        default='monthly'
    )
    experience = models.CharField(max_length=255, blank=True, null=True)
    experience_from = models.PositiveIntegerField(blank=True, null=True)
    experience_to = models.PositiveIntegerField(blank=True, null=True)
    employment_type = models.CharField(
        max_length=50,
        choices=[
            ('full_time', 'Полная занятость'),
            ('part_time', 'Частичная занятость'),
            ('internship', 'Стажировка'),
            ('contract', 'Контракт'),
            ('remote', 'Удалённая работа'),
        ],
        default='full_time'
    )
    schedule = models.CharField(
        max_length=50,
        choices=[
            ('day', 'Дневные смены'),
            ('night', 'Ночные смены'),
            ('flexible', 'Гибкий график'),
            ('shift', 'Сменный график'),
            ('remote', 'Удалённо'),
        ],
        default='day'
    )
    working_hours = models.CharField(max_length=100, blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    experience_required = models.CharField(
        max_length=50,
        choices=[
            ('with_experience', 'с опытом'),
            ('without_experience', 'без опыта'),
        ],
        default='with_experience'
    )
    conditions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} at {self.company.name}'
