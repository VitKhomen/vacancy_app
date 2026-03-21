from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.companies.views import toggle_favorite, hide_vacancy, hide_company

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.homepage_user.urls')),
    # namespace='detail_vacancy' задан всередині
    path('detail/', include('apps.detail_vacancy.urls')),
    path('vacancy/toggle/<int:vacancy_id>/',
         toggle_favorite, name='toggle_favorite'),
    path('vacancy/hide/<int:pk>/', hide_vacancy, name='hide_vacancy'),
    path('company/hide/<int:pk>/', hide_company, name='hide_company'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
