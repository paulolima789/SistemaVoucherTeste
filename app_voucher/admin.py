from django.contrib import admin
from .models import Voucher,Especialidade

# Register your models here.

#colocando na area administrativa do Django
admin.site.register(Voucher)
admin.site.register(Especialidade)
