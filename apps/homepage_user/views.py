from django.views.generic import TemplateView
from django.db.models import Count, Avg

from apps.vacancies.models import Vacancy
from apps.core.models import SiteSettings
from apps.communications.models import Response, Invitation
from .utils import filterd_objects_with_filter_type


class HomePageView(TemplateView):
    template_name = "homepage_user/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        site_settings = SiteSettings.objects.first()
        context["logo"] = site_settings.logo if site_settings else None
        context["main_banner"] = site_settings.main_banner if site_settings else None

        context["total_responses"] = Response.objects.count()
        context["total_invitations"] = Invitation.objects.count()
        context["user_city"] = self.request.user.profile.location if self.request.user.is_authenticated else 'Kiev'

        vacancies = Vacancy.objects.select_related(
            "company", "profession"
        ).annotate(
            feedback_count=Count("company__feedbacks"),
            avg_rating=Avg("company__feedbacks__rating"),
        ).exclude(
            hidden_by__user=self.request.user
            if self.request.user.is_authenticated
            else None
        )

        filter_type = self.request.GET.get("filter")
        vacancies = filterd_objects_with_filter_type(vacancies, filter_type)

        context["vacancies"] = vacancies[:7]

        return context
