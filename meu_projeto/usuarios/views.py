from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("usuarios:login")
    else:
        form = CustomUserCreationForm()
    return render(request, "usuarios/signup.html", {"form": form})
