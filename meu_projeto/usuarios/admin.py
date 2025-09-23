from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Register your models here.
@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    # Campos que aparecem na lista de usuários
    list_display = ('username', 'email', 'is_admin', 'is_staff', 'is_superuser')
    
    # Campos que aparecem no formulário de edição
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações pessoais', {'fields': ('email',)}),
        ('Permissões', {'fields': ('is_active', 'is_admin', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )


