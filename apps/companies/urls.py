from django.urls import path
from .views import toggle_favorite

urlpatterns = [
    path("vacancies/<int:vacancy_id>/favorite/",
         toggle_favorite, name="toggle_favorite"),
]
