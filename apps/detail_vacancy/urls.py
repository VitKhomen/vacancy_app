from django.urls import path
from .views import DetailVacancyView, ComplaintView

app_name = 'detail_vacancy'

urlpatterns = [
    path('<int:pk>/', DetailVacancyView.as_view(), name='detail_vacancy'),
    path('<int:pk>/complaint/', ComplaintView.as_view(), name='submit_complaint'),
]
