from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    
    """Modelo de usuário customizado, herdando de AbstractUser."""

    id = models.AutoField(primary_key=True)
    is_admin = models.BooleanField(default=True, help_text="Designa se o usuário é um administrador", verbose_name="Administrador")

    def __str__(self):
        return self.username
