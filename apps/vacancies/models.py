from django.db import models
from django.conf import settings

from apps.companies.models import Company


class Vacancy(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='vacancies')
    title = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    experience = models.CharField(max_length=255, blank=True, null=True)
    employment_type = models.CharField(
        max_length=50,
        choices=[
            ('full_time', 'Полная занятость'),
            ('part_time', 'Частичная занятость'),
            ('internship', 'Стажировка'),
            ('contract', 'Контракт'),
            ('remote', 'Удалённая работа')
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
            ('remote', 'Удалённо')
        ],
        default='day'
    )
    working_hours = models.CharField(max_length=100, blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    conditions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} at {self.company.name}'
