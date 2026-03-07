from django.db import models


class SiteSettings(models.Model):
    logo = models.ImageField(
        upload_to="site_settings/logo/", verbose_name="Логотип сайта")
    main_banner = models.ImageField(
        upload_to="site_settings/banner/", verbose_name="Главный баннер")

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return "Настройки сайта"
