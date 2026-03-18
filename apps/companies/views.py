from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse

from apps.vacancies.models import Vacancy
from .models import FavoriteVacancy, HiddenVacancy


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
