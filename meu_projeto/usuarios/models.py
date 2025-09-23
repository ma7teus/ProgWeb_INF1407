from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    id = models.AutoField(primary_key=True)
    is_admin = models.BooleanField(default=True, help_text="Designa se o usuário é um administrador", verbose_name="Administrador")

    def __str__(self):
        return self.username
