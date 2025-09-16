from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CarroForm
from .models import Carro
from django.views.decorators.http import require_POST

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


@require_POST
def carro_excluir(request, placa):   # use (request, pk) se for por id
    carro = get_object_or_404(Carro, placa=placa)  # ou get_object_or_404(Carro, pk=pk)
    carro.delete()
    messages.success(request, "Carro excluído com sucesso.")
    return redirect("carros:disponiveis")

def carro_editar(request, placa):
    carro = get_object_or_404(Carro, placa=placa)
    if request.method == "POST":
        form = CarroForm(request.POST, request.FILES, instance=carro)
        if form.is_valid():
            form.save()
            messages.success(request, f"Carro {carro.placa} atualizado com sucesso!")
            return redirect("carros:disponiveis")
    else:
        form = CarroForm(instance=carro)
    return render(request, "carros/editar.html", {"form": form, "carro": carro})