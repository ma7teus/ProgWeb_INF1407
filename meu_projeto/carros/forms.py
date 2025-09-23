from django import forms
from .models import Carro

class CarroForm(forms.ModelForm):
    class Meta:
        model = Carro
        fields = ["placa", "marca", "modelo", "ano", "diaria", "descricao", "imagem"]
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 3}),
        }
