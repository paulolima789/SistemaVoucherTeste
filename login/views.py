from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login2
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def login(request):
    '''Responsavel por validar o usuario'''
    if request.method =='GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        user = authenticate(username=username, password=senha)
        
        if user:
            login2(request,user)
            return redirect('criar')
        else:
            return render(request, 'login.html',{
                                                'erro':'Usuario ou senha incorreto!',
                                                'username': username,
                                                'senha': senha,
                                                })
                                            

def cadastro(request):
    '''responsavel por realizar o cadastro'''
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        username = request.POST.get('username')
        email_form = request.POST.get('email')
        senha = request.POST.get('senha')
        comfirmar_senha = request.POST.get('confirmar_senha')
        
        
        if senha!=comfirmar_senha:
            return render(request, 'cadastro.html',{
                'erroSenha': 'As senhas estão diferentes!',
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email':email_form,
                })
        
        user = User.objects.filter(username=username).filter()
        if user:
                return render(request, 'cadastro.html',{
                'erroUser': 'Esse usuario ja existe!',
                'first_name': first_name,
                'last_name': last_name,
                'email':email_form,
                'senha':senha,
                'comfirmar_senha': comfirmar_senha,
                })
        email = User.objects.filter(email=email_form).filter()
        if email:
                return render(request, 'cadastro.html',{
                'erroEmail': 'Esse email ja existe!',
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'senha':senha,
                'comfirmar_senha': comfirmar_senha,
                })

        user = User.objects.create_user(username=username,email=email_form,password=senha,first_name=first_name,last_name=last_name)
        user.save()
        return redirect('login')


from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('login')
