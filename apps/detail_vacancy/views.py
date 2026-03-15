from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg

from apps.vacancies.models import Vacancy
from apps.core.models import SiteSettings
from apps.companies.models import FeedbackCompany
from .utils import render_stars_html


class DetailVacancyView(LoginRequiredMixin, DetailView):
    model = Vacancy
    template_name = 'detail_vacancy/detail_vacancy.html'
    context_object_name = 'vacancy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy = self.object.exclude(hidden_by_users__user=self.request.user)
        company = vacancy.company

        # Логотип сайта
        site_settings = SiteSettings.objects.first()
        context['logo'] = site_settings.logo if site_settings else None

        # Город пользователя
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'profile'):
            context['user_city'] = user.profile.location
        else:
            context['user_city'] = 'Москва'

        # Все вакансии компании кроме текущей
        context['vacancies_company'] = Vacancy.objects.filter(
            company=company
        ).exclude(pk=vacancy.pk)

        # 2 похожие вакансии не из этой компании
        context['similar_vacancies'] = Vacancy.objects.filter(
            profession=vacancy.profession
        ).exclude(company=company)[:2]

        # 4 последних отзыва компании
        context['feedbacks_company'] = FeedbackCompany.objects.filter(
            company=company
        ).order_by('-created_at')[:4]

        # Средний рейтинг
        result = FeedbackCompany.objects.filter(
            company=company
        ).aggregate(avg=Avg('rating'))
        rating = round(result['avg'] or 0, 1)
        context['rating'] = rating

        # HTML звёзд
        context['stars_rating'] = render_stars_html(rating)

        return context
