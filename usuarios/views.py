from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        confirmar_senha = request.POST.get('confirmar_senha')

        if User.objects.filter(username=username).exists():
            messages.add_message(request, constants.ERROR, 'Usuário já existe')
            return redirect(request.path_info)

        if not senha == confirmar_senha:
            messages.add_message(request, constants.WARNING, 'Senhas diferentes')
            return redirect(request.path_info)
    
        try:
            User.objects.create_user(
                first_name = primeiro_nome,
                last_name=ultimo_nome,
                username=username,
                email=email,
                password=senha
            )
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
        
        messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso')
        return redirect(request.path_info)
    
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            auth_login(request, user)
						# Acontecerá um erro ao redirecionar por enquanto, resolveremos nos próximos passos
            return redirect('/exames/solicitar-exames')
        else:
            messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
            return redirect('/usuarios/login')