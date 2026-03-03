import os
from django.core.exceptions import ValidationError


def validate_avatar_size(image):
    max_size_kb = 5
    if image.size > max_size_kb * 1024 * 1024:
        raise ValidationError(
            f"Размер аватара не должен превышать {max_size_kb} МБ.")


def avatar_upload_path(instance, filename):
    return os.path.join("avatars", str(instance.user.id), filename)
