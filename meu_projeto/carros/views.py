from django.shortcuts import render
from .models import Carro

def carros_disponiveis(request):
    qs = Carro.objects.filter(locatario__isnull=True)  # disponíveis
    return render(request, "carros/disponiveis.html", {"carros": qs})
