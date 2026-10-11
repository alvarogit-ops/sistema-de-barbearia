"""
URL configuration for config project.

Para mais informações: https://docs.djangoproject.com/en/6.1/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('barber_grid.urls')),
]

# Em desenvolvimento, serve os arquivos enviados (media). Em produção, o
# servidor web (nginx etc.) deve servir /media/.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )