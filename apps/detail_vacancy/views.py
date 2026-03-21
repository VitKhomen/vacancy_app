from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.db.models import Avg

from apps.vacancies.models import Vacancy
from apps.core.models import SiteSettings
from apps.companies.models import FeedbackCompany, FavoriteVacancy
from .utils import render_stars_html, years_declension, split_lines
from .forms import ComplaintForm


class DetailVacancyView(LoginRequiredMixin, DetailView):
    model = Vacancy
    template_name = 'detail_vacancy/detail_vacancy.html'
    context_object_name = 'vacancy'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Vacancy.objects.visible_for_user(self.request.user),
            pk=self.kwargs['pk']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy = self.object
        company = vacancy.company
        user = self.request.user

        site_settings = SiteSettings.objects.first()
        context['logo'] = site_settings.logo if site_settings else None

        if hasattr(user, 'profile') and user.profile.location:
            context['user_city'] = user.profile.location
        else:
            context['user_city'] = 'Unknown'

        context['vacancies_company'] = Vacancy.objects.visible_for_user(
            user
        ).filter(company=company).exclude(pk=vacancy.pk)

        context['similar_vacancies'] = Vacancy.objects.visible_for_user(
            user
        ).filter(profession=vacancy.profession).exclude(company=company)[:2]

        context['feedbacks_company'] = FeedbackCompany.objects.filter(
            company=company
        ).order_by('-created_at')[:4]

        result = FeedbackCompany.objects.filter(
            company=company
        ).aggregate(avg=Avg('rating'))
        rating = round(result['avg'] or 0, 1)
        context['rating'] = rating
        context['stars_rating'] = render_stars_html(rating)

        context['experience_required'] = years_declension(
            vacancy.experience_required,
            vacancy.experience_from,
            vacancy.experience_to
        )

        context['responsibilities'] = split_lines(vacancy.responsibilities)
        context['conditions'] = split_lines(vacancy.conditions)

        context['user_favorites'] = set(
            FavoriteVacancy.objects.filter(
                user=user
            ).values_list('vacancy_id', flat=True)
        )

        return context


class ComplaintView(LoginRequiredMixin, CreateView):
    template_name = 'detail_vacancy/complaint.html'
    form_class = ComplaintForm

    def get_vacancy(self):
        return get_object_or_404(Vacancy, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancy'] = self.get_vacancy()
        # logo for base.html
        site_settings = SiteSettings.objects.first()
        context['logo'] = site_settings.logo if site_settings else None
        return context

    def form_valid(self, form):
        complaint = form.save(commit=False)
        complaint.user = self.request.user
        complaint.vacancy = self.get_vacancy()
        complaint.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_vacancy:detail_vacancy', kwargs={'pk': self.kwargs['pk']})
