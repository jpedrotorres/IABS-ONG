from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import MembroLoginForms

# Create your views here.
def hello_world(request):
    return HttpResponse("Hello World")

def membro_login_view(request):
	if request.method == "POST":
		form = MembroLoginForms(request, data=request.POST)

		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect("index")
	else:
		form = MembroLoginForms(request)

		if request.user.is_authenticated:
			return redirect("index")
	return render(request, "contatos/login.html", {"form": form})

@login_required
def index_view(request):
    return render(request, "contatos/parceiro.html")

def logout_confirm_modal_view(request):
	return render(request, "base/system_out_message.html")

def membro_logout_view(request):
	logout(request)
	return redirect('login')
