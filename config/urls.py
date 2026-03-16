from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.companies.views import toggle_favorite

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.homepage_user.urls')),
    path("vacancy/", include("apps.companies.urls")),
    path("detail/", include("apps.detail_vacancy.urls")),
    path('vacancy/toggle/<int:vacancy_id>/',
         toggle_favorite, name='toggle_favorite'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
