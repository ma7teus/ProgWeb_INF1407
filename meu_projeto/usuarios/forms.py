from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class CustomUserCreationForm(UserCreationForm):
    
    """Formulário de criação de usuários customizados."""

    class Meta:
        model = Usuario 
        fields = ("username", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = False
        if commit:
            user.save()
        return user