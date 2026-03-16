from django.urls import path
from .views import DetailVacancyView

urlpatterns = [
    path('<int:pk>/', DetailVacancyView.as_view(), name='detail_vacancy'),
]
