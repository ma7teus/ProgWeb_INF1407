from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Usuario
import re
from django.core.exceptions import ValidationError

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = Usuario 
#         fields = ("username", "email", "telefone", "cpf", "data_nascimento", "endereco", "cidade","estado")  # e outros campos que você queira

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.is_admin = False
#         if commit:
#             user.save()
#         return user

class CustomUserCreationForm(UserCreationForm):
    # Definindo os widgets com classes CSS para aplicar as máscaras
    telefone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control telefone-mask',
            'placeholder': '(11) 99999-9999'
        }),
        label='Telefone'
    )
    
    cpf = forms.CharField(
        max_length=14,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control cpf-mask',
            'placeholder': '123.456.789-00'
        }),
        label='CPF'
    )
    
    data_nascimento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control date-mask',
            'placeholder': 'dd/mm/aaaa',
            'type': 'text'  # Usando text para permitir a máscara personalizada
        }),
        label='Data de Nascimento'
    )

    class Meta:
        model = Usuario 
        fields = ("username", "email", "telefone", "cpf", "data_nascimento", "endereco", "cidade", "estado")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            # Remove todos os caracteres não numéricos
            telefone_limpo = re.sub(r'[^\d]', '', telefone)
            
            # Valida o formato (deve ter 10 ou 11 dígitos)
            if len(telefone_limpo) not in [10, 11]:
                raise ValidationError('Telefone deve ter 10 ou 11 dígitos.')
            
            return telefone_limpo
        return telefone

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            # Remove todos os caracteres não numéricos
            cpf_limpo = re.sub(r'[^\d]', '', cpf)
            
            # Valida se tem 11 dígitos
            if len(cpf_limpo) != 11:
                raise ValidationError('CPF deve ter 11 dígitos.')
            
            # Validação básica de CPF (você pode implementar uma validação mais robusta)
            if cpf_limpo == cpf_limpo[0] * 11:  # Verifica se não são todos iguais
                raise ValidationError('CPF inválido.')
            
            return cpf_limpo
        return cpf

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if data_nascimento:
            # Se o campo vier como string (por causa da máscara), converte para date
            if isinstance(data_nascimento, str):
                try:
                    from datetime import datetime
                    # Remove caracteres não numéricos e reconstrói a data
                    data_limpa = re.sub(r'[^\d]', '', data_nascimento)
                    if len(data_limpa) == 8:
                        dia = data_limpa[:2]
                        mes = data_limpa[2:4]
                        ano = data_limpa[4:]
                        data_nascimento = datetime.strptime(f'{ano}-{mes}-{dia}', '%Y-%m-%d').date()
                    else:
                        raise ValidationError('Data deve estar no formato dd/mm/aaaa.')
                except ValueError:
                    raise ValidationError('Data inválida.')
        
        return data_nascimento

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = False
        if commit:
            user.save()
        return user