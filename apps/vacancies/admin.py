from django.contrib import admin

from .models import Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company', 'employment_type',
                    'schedule', 'created_at')
    list_filter = ("employment_type", "schedule", "created_at")
    search_fields = ("title", "company__name")
