from django.db import models
from django.contrib.auth.models import User
from .choices import ChoicesZona
# Create your models here.

class Especialidade(models.Model):
    nome = models.CharField(max_length=20,unique=True)
    descrição = models.CharField(max_length=30, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.nome
    
class Voucher(models.Model):
    matricula = models.CharField(max_length=30)
    nomeFiliado = models.CharField(max_length=70)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.DO_NOTHING)
    unidade = models.CharField(max_length=10, choices=ChoicesZona.choices)
    consultor = models.CharField(max_length=30)
    dataDaConsulta = models.CharField(max_length=10)
    dataDeGeracao = models.DateField(null=True)
    useuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    
    def __str__(self) -> str:
        return self.nomeFiliado
    
