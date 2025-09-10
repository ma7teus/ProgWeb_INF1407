from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Register your models here.
@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    model = Usuario
    
    list_display = ("username", "email", "is_admin", "telefone", "cpf", "data_nascimento", "cidade", "estado")
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_admin', 'telefone', 'cpf', 'data_nascimento', 'endereco', 'cidade', 'estado')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_admin', 'telefone', 'cpf', 'data_nascimento', 'endereco', 'cidade', 'estado')}),
    )

