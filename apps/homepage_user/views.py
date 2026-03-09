from django.views.generic import TemplateView

from apps.vacancies.models import Vacancy
from core.models import SiteSettings
from communications.models import Response, Invitation


class HomePageView(TemplateView):
    template_name = "homepage_user/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        site_settings = SiteSettings.objects.first()
        context["logo"] = site_settings.logo if site_settings else None
        context["main_banner"] = site_settings.main_banner if site_settings else None

        total_responses = Response.objects.count()
        total_invitations = Invitation.objects.count()
        context["total_responses"] = total_responses
        context["total_invitations"] = total_invitations

        context["vacancies"] = Vacancy.objects.select_related("company", "profession").all()[:7]

        return context