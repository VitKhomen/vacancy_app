from django.views.generic import TemplateView
from django.db.models import Count

from apps.vacancies.models import Vacancy
from apps.core.models import SiteSettings
from apps.communications.models import Response, Invitation
from apps.companies.models import Company


class HomePageView(TemplateView):
    template_name = "homepage_user/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        site_settings = SiteSettings.objects.first()
        context["logo"] = site_settings.logo if site_settings else None
        context["main_banner"] = site_settings.main_banner if site_settings else None

        context["total_responses"] = Response.objects.count()
        context["total_invitations"] = Invitation.objects.count()

        context["vacancies"] = Vacancy.objects.select_related(
            "company", "profession"
        ).annotate(
            feedback_count=Count("company__feedbacks"),
        ).exclude(hidden_vacancies__user=self.request.user).all()[:7]

        return context
