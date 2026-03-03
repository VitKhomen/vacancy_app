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
