from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    """Página inicial (home) do site.

    Carrega a página inicial da aplicação

    Args:
        request (HttpRequest): requisição HTTP.

    Returns:
        HttpResponse: template ``home.html``.
    """
    return render(request, 'home.html', {"is_admin": request.user.is_admin, "username": request.user.username})