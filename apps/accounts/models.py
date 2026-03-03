from django.db import models
from django.conf import settings

from .utils import validate_avatar_size, avatar_upload_path


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(
        upload_to=avatar_upload_path, blank=True, null=True, validators=[validate_avatar_size])
    phone_number = models.CharField(
        max_length=20, blank=True, null=True, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Профіль {self.user.username}"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
