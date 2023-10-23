from django.shortcuts import render,redirect
# permição / registro
from django.contrib.auth import authenticate
from django.contrib.auth import login as login2
from django.contrib.auth.decorators import login_required
# Realizar testes
from django.http import HttpResponse
# Gerenciador de imagens, arquivos e data
'''from PIL import Image'''
import os
# importa a data e hora
from django.utils import timezone
from datetime import datetime
# importando as comfiguraçoes
from django.conf import settings
# Model
from django.db.models import Q
from .models import Voucher, Especialidade
# choices
from .models import ChoicesZona
# Model User
from django.contrib.auth.models import User
#redirecionar / ververce
from django.urls import reverse
from django.http import HttpResponseRedirect
# importe verificador
import re
# Create your views here.

@login_required(login_url="login")
def criar(request,alertstatus=""):
    '''sera responsavel por criar os vouches e arquivar eles'''
    if request.method == 'GET':
        alertstatus = request.session.get('alertstatus')
        #pega a especialidade LIMPEZA ODONTOLOGICA
        try:
            getEspecialidade = Especialidade.objects.get(nome='LIMPEZA ODONTOLOGICA')
        except:
            pass
        # pega a quantidade de voucher sem limpeza odontologica
        try:
            getUser = User.objects.get(username=request.user)
            qtd_voucher = Voucher.objects.filter(useuario__id=getUser.id)
            qtd_voucher = qtd_voucher.exclude(especialidade=getEspecialidade.id)
            contadorSemLimpeza = qtd_voucher.count()
        except:
            pass
        # pega a quantidade de voucher de limpeza odontologica
        try:
            getEspecialidade = Especialidade.objects.get(nome='LIMPEZA ODONTOLOGICA')
            qtd_voucherLimpeza = Voucher.objects.filter(useuario__id=getUser.id,especialidade=getEspecialidade)
            contadorLimpeza = qtd_voucherLimpeza.count()
        except:
            pass
        
        #pega as especialidades
        try:
            allEspecialidade = Especialidade.objects.all()
        except:
            pass
        #pega todos os usuarios
        today = timezone.now()
        allUsers = User.objects.all()
        #verifica os vouchers criados no mes
        user = request.user
        this_month_vouchers = Voucher.objects.filter(useuario=user, dataDeGeracao__month=today.month).count()
        
        if this_month_vouchers >= 10:
            status = "limite atingido"
        else:
            status = ""
        return render(request,'voucher_criar.html',{'status':status,
                                                    'alertstatus':alertstatus,
                                                    'contadorSemLimpeza':contadorSemLimpeza,
                                                    'contadorLimpeza':contadorLimpeza,
                                                    'contadorVocher':this_month_vouchers,
                                                    'allUsers':allUsers,
                                                    'allEspecialidade':allEspecialidade,
                                                    'Zonas': ChoicesZona.choices,
                                                    })
    elif request.method == 'POST':
        today = timezone.now()
        # pega a quantidade de voucher sem limpeza odontologica
        getUser = User.objects.get(username=request.user)
    
        user = request.user    
        this_month_vouchers = Voucher.objects.filter(useuario=user, dataDeGeracao__month=today.month).count()
        
        if (getUser.is_staff == True) or (this_month_vouchers <= 9):
            #pegando nome e sobrenome de quem esta logado
            nomeL = request.user.first_name
            sobrenomeL = request.user.last_name
            #pegando as informaçãoes dos usuarios
            matricula = request.POST.get("matricula")

                
            nomeFiliado = request.POST.get("nomeFiliado")
            
            getEspecialidade = request.POST.get("especialidade")
            especialidade = Especialidade.objects.get(nome=getEspecialidade)
            especialidade = Especialidade.objects.get(id=especialidade.id)
            unidade = request.POST.get("unidade")

            getConsultor = request.POST.get("consultor")

            if (getConsultor == "") or (getConsultor == None):
                consultor = str(nomeL+' '+sobrenomeL)
                userr = User.objects.get(username=request.user)
            else:
                consultor = getConsultor
                userr = User.objects.get(username=consultor)
                consultor = str(userr.first_name+' '+userr.last_name)
                

            
            dataDaConsulta = request.POST.get("dataDaConsulta")
            dataFormatada = datetime.strptime(dataDaConsulta,"%Y-%m-%d")
            dataDaConsulta = datetime.strftime(dataFormatada,"%d/%m/%Y")
            
            dataDeGeracao = today.date()
            
            padrao = r'AM3480\d+'
            if not re.search(padrao,matricula):
                if 'alertstatus' in request.session:
                    status = ""
                    alertstatus = request.session['alertstatus'] = status
                try:
                    #instanciando e guardando no banco de dados
                    voucher = Voucher(
                                    matricula=matricula,
                                    nomeFiliado=nomeFiliado,
                                    especialidade=especialidade,
                                    unidade=unidade,
                                    consultor=consultor,
                                    dataDaConsulta=dataDaConsulta,
                                    dataDeGeracao=dataDeGeracao,
                                    useuario_id=userr.id
                                    )
                    voucher.save()
                    status = 'sucesso'
                except:
                    status = 'error'
            else:
                status = 'A matricula pertence a outra unidade!'
                alertstatus = request.session['alertstatus'] = status
                return redirect('criar')
            
            alertstatus = request.session['alertstatus'] = ''
            unidade = dict(ChoicesZona.choices).get(voucher.unidade, "Desconhecido")
            
            return render(request,'voucher_ver.html',{'status':status,
                                                    'matricula':matricula,
                                                    'nomeFiliado':nomeFiliado,
                                                    'especialidade':especialidade,
                                                    'unidade':unidade,
                                                    'consultor':consultor,
                                                    'dataDaConsulta':dataDaConsulta,
                                                    'dataDeGeracao':dataDeGeracao,
                                                    })
        else:
            return redirect("registros")
        
'''
        #traser tudo do banco
        voucher = Voucher.objects.all()
        #caso queira filtrar
        voucher = Voucher.objects.filter(nomeFiliado="n")
        #validaçao para ver se ja existe no banco de dados
        voucher = Voucher.objects.filter(nomeFiliado="n")
        if voucher.exists():
            pass # se ja existir usuario vai cair aqui
        else:
            pass # se não existir vai cair aqui
        
'''
@login_required(login_url="login")
def ver(request):
    '''ele sera a parte de visualização dos vouches'''
    if request.method == 'POST':
    # usa o proprio horario do django o pradrao e: (07 de abril de 2023)
        # tipos de formatação de hora  data
            # dd/mm/yyyy
      #  formatted_date = data_atual.strftime('%d/%m/%Y')
            # hh:mm:ss
      #  formatted_time = data_atual.strftime('%H:%M:%S')
            # yyyy
      #  week_of_year = data_atual.strftime('%Y')
        '''inicializando codigo'''
        # data_atual = timezone.now()
        try:
            href_id = request.POST.get('voucher')
            voucher = Voucher.objects.filter(id=href_id)
            for voucher1 in voucher:
                matricula = voucher1.matricula
                nomeFiliado = voucher1.nomeFiliado
                especialidade = voucher1.especialidade
                unidade = dict(ChoicesZona.choices).get(voucher1.unidade, "Desconhecido")
                dataDaConsulta = voucher1.dataDaConsulta
                consultor = voucher1.consultor
                dataDeGeracao = voucher1.dataDeGeracao
            
            # visualizar voucher
            return render(request, 'voucher_ver.html', {
                                                        'matricula':matricula,
                                                        'nomeFiliado':nomeFiliado,
                                                        'especialidade':especialidade,
                                                        'unidade':unidade,
                                                        'dataDaConsulta':dataDaConsulta,
                                                        'consultor':consultor,
                                                        'dataDeGeracao':dataDeGeracao
                                                        })
        except:
            matricula = ''
            nomeFiliado = ''
            especialidade = ''
            unidade = ''
            dataDaConsulta = ''
            consultor = ''
            dataDeGeracao = ''
            return render(request, 'voucher_ver.html', {
                                                        'matricula':matricula,
                                                        'nomeFiliado':nomeFiliado,
                                                        'especialidade':especialidade,
                                                        'unidade':unidade,
                                                        'dataDaConsulta':dataDaConsulta,
                                                        'consultor':consultor,
                                                        'dataDeGeracao':dataDeGeracao
                                                        })


@login_required(login_url="login")
def registros(request):
    '''sera a parte de verificar os registros'''
    if request.method == 'GET':
        #pegando o usuario logado e buscando pelo voucher ligado ao usuario
        getUser = User.objects.get(username=request.user)
        if getUser.is_staff == False:
            userr = User.objects.get(username=request.user)
            vouchers = Voucher.objects.filter(useuario__id=userr.id)
        else:
            vouchers = Voucher.objects.all()
        return render(request, 'voucher_registros.html',{'vouchers':vouchers,
                                                         'status':'NaN'
                                                         })
    elif request.method == 'POST':
        pesquisa = request.POST.get('pesquisa')
        if pesquisa:
            vouchers = Voucher.objects.filter(
                    Q(matricula__icontains=pesquisa) |
                    Q(nomeFiliado__icontains=pesquisa) |
                    Q(unidade__icontains=pesquisa) |
                    Q(consultor__icontains=pesquisa)
            )
        else:
            vouchers = Voucher.objects.all()  # Se não houver consulta, retorne todos os objetos
        
        return render(request, 'voucher_registros.html',{'vouchers':vouchers,
                                                         'status':'NaN'
                                                         })


'''
@login_required(login_url="login")
def media(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    elif request.method == 'POST':
        #relogio \ formatação
        data_atual = timezone.now()
        formatted_date = data_atual.strftime('%d/%m/%Y')
        # pega o arquivo no upload
        file = request.FILES.get("my_file")
        img = Image.open(file)
        path = os.path.join(settings.BASE_DIR, f'media/{file.name}-{formatted_date}.pdf')
        img = img.save(path)
        
        return HttpResponse('teste')
'''