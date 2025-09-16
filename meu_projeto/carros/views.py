from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CarroForm
from .models import Carro

def carro_criar(request):
    if request.method == "POST":
        form = CarroForm(request.POST, request.FILES)
        if form.is_valid():
            carro = form.save()  # ⬅️ grava no banco
            messages.success(request, f"Carro {carro.marca} {carro.modelo} cadastrado!")
            return redirect("carros:disponiveis")  # ⬅️ vai pra listagem
    else:
        form = CarroForm()
    return render(request, "carros/cadastrar.html", {"form": form})

def carros_disponiveis(request):
    carros = Carro.objects.filter(locatario__isnull=True).order_by("marca", "modelo")
    return render(request, "carros/disponiveis.html", {"carros": carros})
