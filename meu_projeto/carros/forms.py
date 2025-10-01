from django import forms
from .models import Carro

class CarroForm(forms.ModelForm):
    """Formulário baseado no modelo Carro, usado para cadastrar e editar veículos."""

    class Meta:
        model = Carro
        fields = ["placa", "marca", "modelo", "ano", "diaria", "descricao", "imagem"]
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 3}),
        }
