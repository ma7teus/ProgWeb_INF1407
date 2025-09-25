from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CarroForm
from .models import Carro
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
def carro_criar(request):
    if request.user.is_admin is False:
        messages.error(request, "Apenas administradores podem criar carros.")
        return redirect("carros:disponiveis")
    
    if request.method == "POST":
        form = CarroForm(request.POST, request.FILES)
        if form.is_valid():
            carro = form.save()
            messages.success(request, f"Carro {carro.marca} {carro.modelo} cadastrado!")
            return redirect("carros:disponiveis")
    else:
        form = CarroForm()
    return render(request, "carros/cadastrar.html", {"form": form})

@login_required
def carros_disponiveis(request):
    carros = Carro.objects.filter(locatario__isnull=True).order_by("marca", "modelo")
    return render(request, "carros/disponiveis.html", {"carros": carros, "is_admin": request.user.is_admin})

@login_required
@require_POST
def carro_excluir(request, placa):   # use (request, pk) se for por id
    if request.user.is_admin is False:
        messages.error(request, "Apenas administradores podem excluir carros.")
        return redirect("carros:disponiveis")
    
    carro = get_object_or_404(Carro, placa=placa)  # ou get_object_or_404(Carro, pk=pk)
    carro.delete()
    messages.success(request, "Carro excluído com sucesso.")
    return redirect("carros:disponiveis")

@login_required
def carro_editar(request, placa):
    if request.user.is_admin is False:
        messages.error(request, "Apenas administradores podem editar carros.")
        return redirect("carros:disponiveis")
    
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

@login_required
def alugar_carro(request, placa):
    """Atribui o carro ao usuário logado, se estiver disponível."""
    if request.method != "POST":
        return redirect("carros:disponiveis")

    carro = get_object_or_404(Carro, placa=placa)

    if carro.locatario_id is not None:
        messages.error(request, "Este carro já está alugado.")
        return redirect("carros:disponiveis")

    carro.locatario = request.user
    carro.save()
    messages.success(request, f"Você alugou o {carro.marca} {carro.modelo}.")
    return redirect("carros:alugados")


@login_required
def carros_alugados(request):
    """Lista apenas os carros alugados pelo usuário logado."""
    if request.user.is_admin:
        title = "Carros alugados"
        carros = Carro.objects.filter(locatario__isnull=False).order_by("marca", "modelo")
    else:
        title = "Meus carros alugados"
        carros = Carro.objects.filter(locatario=request.user).order_by("marca", "modelo")
    
    return render(request, "carros/alugados.html", {"carros": carros, "title": title, "is_admin": request.user.is_admin})

@login_required
@require_POST
def encerrar_aluguel(request, placa):
    # Garante que só o dono (ou um admin) encerra
    if request.user.is_staff:
        carro = get_object_or_404(Carro, placa=placa)
    else:
        carro = get_object_or_404(Carro, placa=placa, locatario=request.user)

    carro.locatario = None
    carro.save()
    messages.success(request, "Aluguel encerrado. O carro voltou para a lista de disponíveis.")
    return redirect("carros:disponiveis")