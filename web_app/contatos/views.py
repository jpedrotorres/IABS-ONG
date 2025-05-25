from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import MembroLoginForms

# Create your views here.
def membro_login_view(request):
	if request.method == 'post':
		form = MembroLoginForms(request, data=request.POST)

		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('index')
			else:
				form.add_error(None, "Nome de usuário ou senha inválidos.")
	else:
		form = MembroLoginForms(request)
	return render(request, 'contatos/login.html', {'form': form})

@login_required
def index(Request):
    return HttpResponse("Hello World")
