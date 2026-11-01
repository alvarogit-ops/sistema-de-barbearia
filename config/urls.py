"""
URL configuration for config project.

Para mais informações: https://docs.djangoproject.com/en/6.1/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from django.conf.urls.static import static
from django.conf import settings
from barber_grid import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/painel/', views.painel_admin, name='painel_admin'),
    path('', include('barber_grid.urls'))

]


urlpatterns += static(
    settings.MEDIA_URL,
    document_root = settings.MEDIA_ROOT
)
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
