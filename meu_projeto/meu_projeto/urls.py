from django.contrib import admin
from django.urls import path, include
from meu_app import views as pages  
from django.conf.urls.static import static
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", pages.home, name="home"),
    path("carros/", include("carros.urls", namespace="carros")),
    path("usuarios/", include("usuarios.urls", namespace="usuarios")),

    path('accounts/password_reset/',
         PasswordResetView.as_view(
             template_name='seguranca/password_reset_form.html',
             success_url=reverse_lazy('sec-password_reset_done'),
             html_email_template_name='seguranca/password_reset_email.html',
             subject_template_name='seguranca/password_reset_subject.txt',
             from_email='webmaster@localhost',
         ),
         name='password_reset'),

    path('accounts/password_reset_done/',
         PasswordResetDoneView.as_view(
             template_name='seguranca/password_reset_done.html'
         ),
         name='sec-password_reset_done'),

    path('accounts/password_reset_confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='seguranca/password_reset_confirm.html',
             success_url=reverse_lazy('sec-password_reset_complete')
         ),
         name='password_reset_confirm'),

    path('accounts/password_reset_complete/',
         PasswordResetCompleteView.as_view(
             template_name='seguranca/password_reset_complete.html'
         ),
         name='sec-password_reset_complete'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)