from django.contrib import admin
from .models import Carro

# Register your models here.
@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
    list_display = ("marca", "modelo", "ano", "preco", "criado_em")