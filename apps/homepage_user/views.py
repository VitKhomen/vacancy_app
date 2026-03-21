from django.views.generic import TemplateView
from django.db.models import Avg, Count

from apps.vacancies.models import Vacancy
from apps.core.models import SiteSettings
from apps.communications.models import Response, Invitation
from apps.companies.models import FavoriteVacancy
from .utils import filterd_objects_with_filter_type


class HomePageView(TemplateView):
    template_name = "homepage_user/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Site logo & banner
        site_settings = SiteSettings.objects.first()
        context["logo"] = site_settings.logo if site_settings else None
        context["main_banner"] = site_settings.main_banner if site_settings else None

        # Counters
        context["total_responses"] = Response.objects.count()
        context["total_invitations"] = Invitation.objects.count()

        # Vacancies — exclude hidden vacancies and hidden companies
        vacancies = Vacancy.objects.visible_for_user(
            self.request.user
        ).select_related(
            "company", "profession"
        ).annotate(
            avg_rating=Avg("company__feedbacks__rating"),
            feedback_count=Count("company__feedbacks"),
        )

        # Filter by GET param using utility function
        filter_param = self.request.GET.get("filter")
        vacancies = filterd_objects_with_filter_type(vacancies, filter_param)

        context["vacancies"] = vacancies[:20]

        # IDs of vacancies favourited by the current user
        if self.request.user.is_authenticated:
            context["user_favorites"] = set(
                FavoriteVacancy.objects.filter(
                    user=self.request.user
                ).values_list("vacancy_id", flat=True)
            )
        else:
            context["user_favorites"] = set()

        return context
