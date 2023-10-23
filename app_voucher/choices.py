from django.db.models import TextChoices

class ChoicesZona(TextChoices):
    ZONA_LESTE = ('ZL', 'Zona Leste')
    CIDADE_NOVA = ('CN', 'Cidade Nova')
    CENTRO = ('C', 'Centro')
    SANTO_ANTONIO = ('S', 'Santo Antônio')
    OUTROS = ('O', 'Outros')