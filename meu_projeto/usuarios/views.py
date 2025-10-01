from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def signup(request):
    """Cria uma nova conta de usuário e faz login automático.

    - GET: exibe o formulário de cadastro.
    - POST: valida, cria o usuário e autentica, redirecionando para a home.

    Args:
        request (HttpRequest): requisição HTTP.

    Returns:
        HttpResponse: formulário ou redirecionamento para ``home``.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("usuarios:login")
    else:
        form = CustomUserCreationForm()
    return render(request, "usuarios/signup.html", {"form": form})
