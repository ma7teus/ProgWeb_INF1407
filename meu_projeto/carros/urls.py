from django.urls import path
from . import views

app_name = "carros"

urlpatterns = [
    path("disponiveis/", views.carros_disponiveis, name="disponiveis"),
    path("novo/", views.carro_criar, name="cadastrar"),
    path("<str:placa>/excluir/", views.carro_excluir, name="excluir"),
    path("<str:placa>/editar/", views.carro_editar, name="editar"),  

]
