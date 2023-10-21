from django.db.models import TextChoices

class ChoicesZona(TextChoices):
    ZONA_LESTE = ('ZL', 'Zona Leste')
    CIDADE_NOVA = ('CN', 'Cidade Nova')
    CENTRO = ('C', 'Centro')
    OUTROS = ('O', 'Otros')