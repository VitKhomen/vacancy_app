from django.urls import path
from .views import toggle_favorite, hide_vacancy

urlpatterns = [
    path("<int:vacancy_id>/favorite/",
         toggle_favorite, name="toggle_favorite"),
    path("vacancy/hide/<int:pk>/", hide_vacancy, name="hide_vacancy"),
]
