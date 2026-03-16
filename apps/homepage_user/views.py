from django.views.generic import TemplateView
from django.db.models import Avg, Count

from apps.vacancies.models import Vacancy
from apps.core.models import SiteSettings
from apps.communications.models import Response, Invitation
from apps.companies.models import FavoriteVacancy


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

        # Vacancies with annotated rating & feedback count
        vacancies = Vacancy.objects.select_related(
            "company", "profession"
        ).annotate(
            avg_rating=Avg("company__feedbacks__rating"),
            feedback_count=Count("company__feedbacks"),
        )

        # Filter by GET param
        filter_param = self.request.GET.get("filter")
        if filter_param == "part_time":
            vacancies = vacancies.filter(employment_type="part_time")
        elif filter_param == "without_experience":
            vacancies = vacancies.filter(
                experience_required="without_experience")
        elif filter_param == "internship":
            vacancies = vacancies.filter(employment_type="internship")
        elif filter_param == "remote":
            vacancies = vacancies.filter(employment_type="remote")

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
