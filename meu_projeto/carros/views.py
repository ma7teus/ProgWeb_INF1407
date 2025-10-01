from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CarroForm
from .models import Carro
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
def carro_criar(request):
    """Cria um novo carro no sistema.

    - GET: exibe o formulário vazio.
    - POST: valida e salva um novo registro; em sucesso, redireciona para a listagem
      de disponíveis e mostra uma mensagem

    Args:
        request (HttpRequest): requisição HTTP

    Returns:
        HttpResponse: formulário ou redirecionamento para ``carros:disponiveis``
    """
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
    """Renderiza a listagem de carros disponíveis para aluguel.

    Retorna uma página com os veículos cujo campo ``locatario`` está vazio.
    Se o usuário estiver autenticado, a página pode exibir ações (alugar/editar/excluir)
    de acordo com as permissões configuradas.

    Args:
        request (HttpRequest): requisição HTTP.

    Returns:
        HttpResponse: template ``carros/disponiveis.html`` com o queryset de carros disponíveis.
    """
    carros = Carro.objects.filter(locatario__isnull=True).order_by("marca", "modelo")
    return render(request, "carros/disponiveis.html", {"carros": carros, "is_admin": request.user.is_admin})

@login_required
@require_POST
def carro_excluir(request, placa):
    """Exclui um carro definitivamente.

    Requer método POST por segurança (evita deleção via GET).
    Após excluir, redireciona para a listagem de disponíveis.

    Args:
        request (HttpRequest): requisição HTTP.
        placa (str): placa do veículo.

    Returns:
        HttpResponseRedirect: redireciona para ``carros:disponiveis``.
    """
    if request.user.is_admin is False:
        messages.error(request, "Apenas administradores podem excluir carros.")
        return redirect("carros:disponiveis")
    
    carro = get_object_or_404(Carro, placa=placa) 
    carro.delete()
    messages.success(request, "Carro excluído com sucesso.")
    return redirect("carros:disponiveis")

@login_required
def carro_editar(request, placa):
    """Edita os dados de um carro existente.

    Localiza o carro pela placa e:
    - GET: exibe o formulário preenchido.
    - POST: valida e salva alterações; em sucesso, redireciona para a listagem.

    Args:
        request (HttpRequest): requisição HTTP.
        placa (str): placa do veículo (PK no modelo).

    Returns:
        HttpResponse: formulário de edição ou redirecionamento.
    """
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
    """Atribui o carro ao usuário autenticado (inicia o aluguel).

    Regras:
    - Somente se o carro estiver disponível (``locatario`` nulo).
    - Em sucesso, redireciona para a página de ``carros:alugados``.

    Args:
        request (HttpRequest): requisição HTTP.
        placa (str): placa do veículo.

    Returns:
        HttpResponseRedirect: redireciona para `carros:alugados`` ou ``carros:disponiveis`` com mensagem.
    """
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
    """Lista os carros alugados pelo usuário autenticado.

    Args:
        request (HttpRequest): requisição HTTP.

    Returns:
        HttpResponse: template ``carros/alugados.html`` com os carros do usuário.
    """
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
    """Encerra o aluguel de um carro, removendo a vinculação com o usuário.

    Permite:
    - O próprio locatário encerrar o seu aluguel.
    - Admin encerrar o aluguel de qualquer carro.

    Em sucesso, o carro volta a aparecer na lista de disponíveis.

    Args:
        request (HttpRequest): requisição HTTP.
        placa (str): placa do veículo.

    Returns:
        HttpResponseRedirect: redireciona para ``carros:disponiveis``.
    """

    if request.user.is_staff:
        carro = get_object_or_404(Carro, placa=placa)
    else:
        carro = get_object_or_404(Carro, placa=placa, locatario=request.user)

    carro.locatario = None
    carro.save()
    messages.success(request, "Aluguel encerrado. O carro voltou para a lista de disponíveis.")
    return redirect("carros:disponiveis")