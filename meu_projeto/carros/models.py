from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal

PLACA_REGEX = r'^[A-Z]{3}\d{4}$|^[A-Z]{3}\d[A-Z]\d{2}$'  # ABC1234 ou ABC1D23 (Mercosul)

class Carro(models.Model):
    # NOVO: Placa
    placa = models.CharField(
        max_length=7,
        primary_key=True,   # ⬅️ agora é a PK
        validators=[RegexValidator(PLACA_REGEX, message="Placa inválida.")],
        help_text="Ex.: ABC1234 ou ABC1D23"

    )
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ano = models.PositiveIntegerField()
    diaria = models.DecimalField(
        max_digits=8, decimal_places=2,
        validators=[MinValueValidator(0)],
        default=Decimal("100.00")
    )
    descricao = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='carros/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    #locatário (pode ser nulo quando o carro estiver disponível)
    locatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='carros_alugados'
    )

    class Meta:
        ordering = ["marca", "modelo", "placa"]

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.ano}) - {self.placa}"

    @property
    def disponivel(self) -> bool:
        return self.locatario_id is None

    def clean(self):
        ano_atual = date.today().year
        if self.ano < 1980 or self.ano > ano_atual + 1:
            raise ValidationError({"ano": "Ano fora da faixa permitida."})
