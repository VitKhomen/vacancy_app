from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

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
@require_POST
def toggle_hidden_vacancy(request):
    vacancy_id = request.POST.get("vacancy_id")
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)

    hidden, created = HiddenVacancy.objects.get_or_create(
        user=request.user, vacancy=vacancy)

    if not created:
        hidden.delete()
        return JsonResponse({"status": "removed"})
    else:
        return JsonResponse({"status": "hidden"})
