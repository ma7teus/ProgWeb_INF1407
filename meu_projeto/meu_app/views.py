from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html', {"is_admin": request.user.is_admin, "username": request.user.username})