from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Usuario
import re
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario 
        fields = ("username", "email")  # e outros campos que você queira

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = False
        if commit:
            user.save()
        return user