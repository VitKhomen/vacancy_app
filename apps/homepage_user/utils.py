from apps.vacancies.models import Vacancy


FILTER_MAP = {
    'part_time':          {'employment_type': 'part_time'},
    'without_experience': {'experience_required': 'without_experience'},
    'internship':         {'employment_type': 'internship'},
    'remote':             {'schedule': 'remote'},
}


def filterd_objects_with_filter_type(queryset, filter_type):
    """
    Фильтрует queryset по переданному filter_type.
    Если filter_type не найден в FILTER_MAP — возвращает queryset без изменений.
    """
    filters = FILTER_MAP.get(filter_type)
    if filters:
        return queryset.filter(**filters)
    return queryset
