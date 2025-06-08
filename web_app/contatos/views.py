from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django import forms
import json

from .models import Parceiro, Reuniao
from .forms import MembroLoginForms, MembroForms, ParceiroForms, ReuniaoForms

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
				return redirect("parceiro_page")
	else:
		form = MembroLoginForms(request)

		if request.user.is_authenticated:
			return redirect("parceiro_page")
	return render(request, "contatos/login.html", {"form": form})

@login_required
def index_view(request):
    return render(request, "contatos/index.html")

@login_required
def parceiro_view(request):
	parceiros = Parceiro.objects.all()

	context={
		"parceiros": parceiros,
		"pagina": {
			"tipo": "parceiro"
		}
	}

	return render(request, "contatos/parceiro.html", context)

@login_required
def reuniao_view(request):
	reunioes=Reuniao.objects.all()
	context={
		"reunioes": reunioes,
		"pagina": {
			"tipo": "reuniao"
		}
	}

	return render(request, "contatos/reuniao.html", context)

def get_model_and_form(entity_type):
	if entity_type=="parceiro":
		return Parceiro, ParceiroForms, "parceiro", "parceiro_page", "parceiro_detail", "parceiro_edit"

	elif entity_type=="reuniao":
		return Reuniao, ReuniaoForms, "reuniao", "reuniao_page", "reuniao_detail", "reuniao_edit"

	else:
		return None, None, None, None

@login_required
def generic_detail_view(request, entity_type, pk):
	Model, Form, object_name, page_list, page_detail, page_edit=get_model_and_form(entity_type)

	if not Model:
		raise Http404("Tipo de entidade inválido.")

	obj = get_object_or_404(Model, pk=pk)

	form = Form(instance=obj)

	for field_name, field_object in form.fields.items():
		if (isinstance(field_object.widget, forms.Select) or
			isinstance(field_object.widget, forms.ClearableFileInput) or
			isinstance(field_object.widget, forms.RadioSelect) or
			isinstance(field_object.widget, forms.CheckboxSelectMultiple)):
			field_object.widget.attrs['disabled'] = True

		else:
			field_object.widget.attrs['readonly'] = True

	context = {
		'object_name': object_name,
		'form': form,
		'edit_url': reverse(page_edit, args=[pk]),
	}

	return render(request, "base/base_info_page.html", context)

@login_required
def generic_create_view(request, entity_type):
	Model, Form, object_name, page_list, page_detail, page_edit=get_model_and_form(entity_type)

	if not Model:
		raise Http404("Tipo de entidade inválido.")

	if request.method == 'POST':
		form = Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse(page_list))
	else:
		form = Form()

	context = {
		"object_name": object_name,
		"form": form,
		'form_action_url': request.path,
		'action_text': 'Criar Novo'
	}

	return render(request, "base/base_form_page.html", context)

@login_required
def generic_edit_view(request, entity_type, pk):
	Model, Form, object_name, page_list, page_datail, page_edit=get_model_and_form(entity_type)

	if not Model:
		raise Http404("Tipo de entidade inválido.")

	obj = get_object_or_404(Model, pk=pk)

	if request.method == 'POST':
		form = Form(request.POST, instance=obj)
		if form.is_valid():
			form.save()
			return redirect(reverse(page_detail, args=[pk]))
	else:
		form = Form(instance=obj)

	context = {
		"object_name": object_name,
		"form": form,
		'action_text': 'editar'
	}

	return render(request, "base/base_form_page.html", context)


@login_required
def logout_confirm_modal_view(request):
	try:
		if request.method=="POST":
			data=json.loads(request.body)

			modal_title = data.get('title', 'Atenção!')
			modal_message = data.get('message', 'Confirma esta ação?')
			modal_confirm_url = data.get('confirm_url', '#')
			modal_confirm_text = data.get('confirm_text', 'Confirmar')

			modal_title="atençao! fechando sistema"
			modal_message="você tem certeza que deseja sair?"
			modal_confirm_url=reverse("logout")
			modal_confirm_text="sair"

			context={
				'modal_title': modal_title,
				'modal_message': modal_message,
				'modal_confirm_url': modal_confirm_url,
				'modal_confirm_text': modal_confirm_text,
			}
		else:
			context= {}

		return render(request, "base/base_message.html", context)

	except json.JSONDecodeError:
		return JsonResponse({'error': 'Requisição JSON inválida.'}, status=400)
	except Exception as e:
		return JsonResponse({'error': str(e)}, status=500)

def membro_logout_view(request):
	logout(request)
	return redirect('login')
