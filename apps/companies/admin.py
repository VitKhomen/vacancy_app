from django.contrib import admin

from .models import Company, FeedbackCompany, FavoriteVacancy


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'website',
                    'created_at', 'average_rating_display')
    list_filter = ("created_at",)
    search_fields = ("name", "owner__username")

    def average_rating_display(self, obj):
        return obj.average_rating()
    average_rating_display.short_description = 'Average Rating'


@admin.register(FeedbackCompany)
class FeedbackCompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'comment', 'rating', 'created_at')
    list_filter = ("created_at",)
    search_fields = ("company__name", "comment")


@admin.register(FavoriteVacancy)
class FavoriteVacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vacancy', 'created_at')
    list_filter = ("created_at",)
    search_fields = ("user__username", "vacancy__title")
