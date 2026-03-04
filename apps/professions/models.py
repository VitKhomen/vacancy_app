from tabnanny import verbose

from django.db import models
from django.conf import settings


class CategoryProfession(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Category Profession"
        verbose_name_plural = "Categories Profession"

    def __str__(self):
        return self.name


class Profession(models.Model):
    category = models.ForeignKey(
        CategoryProfession, on_delete=models.CASCADE, related_name='professions')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Profession"
        verbose_name_plural = "Professions"

    def __str__(self):
        return self.name
