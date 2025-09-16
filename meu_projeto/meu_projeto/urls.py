from django.contrib import admin
from django.urls import path, include
from meu_app import views as pages  # sua home atual
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", pages.home, name="home"),
    path("carros/", include("carros.urls", namespace="carros")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)