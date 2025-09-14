from django.contrib import admin
from django.urls import path, include
from meu_app import views as pages  # sua home atual

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", pages.home, name="home"),
    path("carros/", include("carros.urls", namespace="carros")),
]
