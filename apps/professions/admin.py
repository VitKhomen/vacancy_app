from django.contrib import admin
from .models import CategoryProfession, Profession


class ProfessionInline(admin.TabularInline):
    model = Profession
    extra = 1


@admin.register(CategoryProfession)
class CategoryProfessionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("name",)
    search_fields = ("name",)
    inlines = [ProfessionInline]


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_filter = ("category",)
    search_fields = ("name", "category__name")
