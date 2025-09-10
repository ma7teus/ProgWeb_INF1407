from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    id = models.AutoField(primary_key=True)
    is_admin = models.BooleanField(default=False, help_text="Designa se o usuário é um administrador", verbose_name="Administrador")
    telefone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Número de telefone")
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True, verbose_name="CPF")
    data_nascimento = models.DateField(blank=True, null=True, verbose_name="Data de nascimento")
    endereco = models.CharField(max_length=255, blank=True, null=True, verbose_name="Endereço")
    cidade = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cidade")
    estado = models.CharField(max_length=50, blank=True, null=True, verbose_name="Estado")

    def __str__(self):
        return f"{self.username} ({self.get_tipo_usuario_display()})"
