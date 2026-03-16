from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from apps.vacancies.models import Vacancy
from apps.core.models import SiteSettings
from apps.companies.models import FeedbackCompany
from .utils import render_stars_html, years_declension, split_lines


class DetailVacancyView(LoginRequiredMixin, DetailView):
    model = Vacancy
    template_name = 'detail_vacancy/detail_vacancy.html'
    context_object_name = 'vacancy'

    def get_object(self, queryset=None):
        return get_object_or_404(Vacancy, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy = self.object
        company = vacancy.company

        # Site logo
        site_settings = SiteSettings.objects.first()
        context['logo'] = site_settings.logo if site_settings else None

        # User city from profile
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.location:
            context['user_city'] = user.profile.location
        else:
            context['user_city'] = 'Unknown'

        # All vacancies of the same company except current
        context['vacancies_company'] = Vacancy.objects.filter(
            company=company
        ).exclude(pk=vacancy.pk)

        # 2 similar vacancies from other companies
        context['similar_vacancies'] = Vacancy.objects.filter(
            profession=vacancy.profession
        ).exclude(company=company)[:2]

        # 4 latest company reviews
        context['feedbacks_company'] = FeedbackCompany.objects.filter(
            company=company
        ).order_by('-created_at')[:4]

        # Average rating
        result = FeedbackCompany.objects.filter(
            company=company
        ).aggregate(avg=Avg('rating'))
        rating = round(result['avg'] or 0, 1)
        context['rating'] = rating

        # Stars HTML
        context['stars_rating'] = render_stars_html(rating)

        # Experience string
        context['experience_required'] = years_declension(
            vacancy.experience_required,
            vacancy.experience_from,
            vacancy.experience_to
        )

        # Responsibilities and conditions as lists
        context['responsibilities'] = split_lines(vacancy.responsibilities)
        context['conditions'] = split_lines(vacancy.conditions)

        # IDs of vacancies favourited by the current user
        from apps.companies.models import FavoriteVacancy
        context['user_favorites'] = set(
            FavoriteVacancy.objects.filter(
                user=self.request.user
            ).values_list('vacancy_id', flat=True)
        )

        return context
