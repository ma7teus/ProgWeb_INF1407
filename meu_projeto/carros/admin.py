from django.contrib import admin
from .models import Carro

@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
    list_display = ("placa", "marca", "modelo", "ano", "diaria", "locatario", "criado_em")
    search_fields = ("placa", "marca", "modelo")
    list_filter = ("ano",)
    autocomplete_fields = ("locatario",)
