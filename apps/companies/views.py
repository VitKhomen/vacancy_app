from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse

from apps.vacancies.models import Vacancy
from .models import Company, FavoriteVacancy, HiddenVacancy, HiddenCompany


@login_required
def toggle_favorite(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    favorite, created = FavoriteVacancy.objects.get_or_create(
        user=request.user,
        vacancy=vacancy
    )
    if not created:
        favorite.delete()
        return JsonResponse({"status": "removed"})
    return JsonResponse({"status": "added"})


@login_required
def hide_vacancy(request, pk):
    if request.method == "POST":
        vacancy = get_object_or_404(Vacancy, pk=pk)
        HiddenVacancy.objects.get_or_create(user=request.user, vacancy=vacancy)
        messages.success(
            request, "Вакансія прихована і більше не буде відображатись.")
    return redirect("homepage_user:homepage")


@login_required
def hide_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    _, created = HiddenCompany.objects.get_or_create(
        user=request.user,
        company=company
    )
    if created:
        messages.success(
            request, "Компанія прихована і більше не буде відображатись.")
    else:
        messages.success(request, "Компанія вже прихована.")
    return redirect("homepage_user:homepage")
