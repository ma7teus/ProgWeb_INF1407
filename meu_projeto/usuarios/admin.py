from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Register your models here.
@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    model = Usuario  
    list_display = ("username", "email", "is_admin")


