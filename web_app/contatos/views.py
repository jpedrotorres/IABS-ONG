from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django import forms
import json

from .models import MembroIabs, Parceiro, Reuniao
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
def membro_view(request):
	return generic_list_view(request, "membro")

@login_required
def parceiro_view(request):
	return generic_list_view(request, "parceiro")

@login_required
def reuniao_view(request):
	return generic_list_view(request, "reuniao")

def get_model_and_form(entity_type):
	if entity_type=="membro":
		return MembroIabs, MembroForms, "membro", "membro_page", "membro_detail", "membro_edit"

	elif entity_type=="parceiro":
		return Parceiro, ParceiroForms, "parceiro", "parceiro_page", "parceiro_detail", "parceiro_edit"

	elif entity_type=="reuniao":
		return Reuniao, ReuniaoForms, "reuniao", "reuniao_page", "reuniao_detail", "reuniao_edit"

	else:
		return None, None, None, None, None, None

@login_required
def generic_list_view(request, entity_type):
	Model, _, object_name, _, page_detail, _ = get_model_and_form(entity_type)

	if entity_type == "membro":
		template_path= "contatos/membro.html"
		objects= "membros"
	elif entity_type == "parceiro":
		template_path= "contatos/parceiro.html"
		objects= "parceiros"
	elif entity_type == "reuniao":
		template_path= "contatos/reuniao.html"
		objects= "reunioes"

	if not Model:
		raise Http404("Tipo de entidade inválido.")
	
	search_term = request.GET.get("obj", "").strip()
	queryset = Model.objects.all()
	
	if search_term:
		if entity_type == "parceiro":
			queryset = queryset.filter(
				Q(nome__icontains=search_term) | Q(razao_social__icontains=search_term)
			)
		elif entity_type == "reuniao":
			queryset = queryset.filter(
				Q(assunto__icontains=search_term) | Q(parceiros__nome__icontains=search_term) | Q(parceiros__razao_social__icontains=search_term) | Q(membros__nome__icontains=search_term)
			)
	
	context = {
		'object_name': object_name,
		objects: queryset,
		'search_term': search_term,
	}

	return render(request, template_path, context)
	

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
		"back_url": reverse(page_list)
	}

	return render(request, "base/base_info_page.html", context)

@login_required
def generic_create_view(request, entity_type):
	Model, Form, object_name, page_list, page_detail, page_edit=get_model_and_form(entity_type)

	if not Model:
		raise Http404("Tipo de entidade inválido.")

	if request.method == 'POST':
		form = Form(request.POST, request.FILES)
		if form.is_valid():
			obj= form.save()
			
			if request.headers.get('x-requested-with') == 'XMLHttpRequest':
				return JsonResponse({
					'success': True,
					'pk': obj.pk,
					'detail_url': reverse(page_detail, args=[obj.pk])
				})
			else:
				return redirect(reverse(page_list))
				
		else:
			if request.headers.get('x-requested-with') == 'XMLHttpRequest':
				return JsonResponse({
					'error': 'Erro de validação',
					'errors': form.errors
				}, status=400)
			
	else:
		form = Form()

	context = {
		"object_name": object_name,
		"form": form,
		'form_action_url': request.path,
		'action_text': 'Criar Novo',
		"back_url": reverse(page_list),
		'entity_type': entity_type,
		'btn_confirmar_form': 'cadastro',
		'object_id': ''
	}

	return render(request, "base/base_form_page.html", context)

@login_required
def generic_edit_view(request, entity_type, pk):
	Model, Form, object_name, page_list, page_detail, page_edit=get_model_and_form(entity_type)

	if not Model:
		raise Http404("Tipo de entidade inválido.")

	obj = get_object_or_404(Model, pk=pk)

	if request.method == 'POST':
		form = Form(request.POST, request.FILES, instance=obj)
		if form.is_valid():
			form.save()
			
			if request.headers.get('x-requested-with') == 'XMLHttpRequest':
				return JsonResponse({
					'success': True,
					'pk': obj.pk,
					'detail_url': reverse(page_detail, args=[obj.pk])
				})
			else:
				return redirect(reverse(page_detail, args=[pk]))
		else:
			if request.headers.get('x-requested-with') == 'XMLHttpRequest':
				return JsonResponse({
					'error': "Erro de validação",
					'errors': form.errors
				}, status=400)
	else:
		form = Form(instance=obj)

	context = {
		"object_name": object_name,
		"form": form,
		'action_text': 'editar',
		"back_url": reverse(page_detail, args=[pk]),
		"btn_confirmar_form": "editar",
		'entity_type': entity_type,
		'object_id': pk
	}

	return render(request, "base/base_form_page.html", context)

@login_required
def generic_alter_modal_view(request):
	if request.method!="POST":
		return JsonResponse({'error': 'Método não permitido.'}, status=405)
	
	try:
		data = json.loads(request.body)
		modal_type = data.get('type', 'generic')
		
		entity= data.get("entity_type")
		object_id= data.get("object_id")
		current_action = data.get("action", modal_type)
		
		if not entity:
			return JsonResponse({'error': 'Parâmetros entity_type é obrigatório.'}, status=400)
		
		Model, Form, object_name, page_list, page_detail, page_edit=get_model_and_form(entity)
		
		if not Model:
			return JsonResponse({'error': 'Tipo de entidade inválido.'}, status=400)
		

		modal_confirm_text = "confirmar"
		modal_title= "salvando informações"
		modal_message=data.get('message', 'Confirma esta ação?')
		modal_confirm_url="#"
		
		if modal_type == 'cadastro':
			modal_title = "Finalizar Cadastro"
			modal_message="deseja finalizar o cadastro?"
			
			modal_confirm_url = reverse(page_list)

		elif modal_type == "editar":
			modal_title = f"Alterar {object_name}"
			modal_message="deseja alterar os dados?"
			
			if object_id and str(object_id).isdigit() and int(object_id) > 0:
				try:
					modal_confirm_url = reverse(page_detail, args=[object_id])
				except Exception:
					modal_confirm_url = reverse(page_list)
			else:
				return JsonResponse({'error': 'PK obrigatório para modal de edição.'}, status=400)
		
		context={
			'modal_title': modal_title,
			'modal_message': modal_message,
			'modal_confirm_url': modal_confirm_url,
			'modal_confirm_text': modal_confirm_text,
			'modal_type': modal_type
			}
		
		return render(request, "base/base_message.html", context)

	except json.JSONDecodeError:
		return JsonResponse({'error': 'Requisição JSON inválida.'}, status=400)
	except Exception as e:
		return JsonResponse({'error': str(e)}, status=500)


@login_required
def warning_relatorio_modal_view(request, pk):
	try:
		obj=get_object_or_404(Reuniao, pk=pk)

		if request.method=="GET":
			tem_relatorio = bool(obj.relatorio)
			return JsonResponse({
				'tem_relatorio': tem_relatorio,
				'reuniao_id': obj.pk,
				'relatorio_url': obj.relatorio.url if obj.relatorio else ''
			})


		elif request.method=="POST":
			data=json.loads(request.body)

			modal_title="relatório não encontrado!"
			modal_message="não foi possível acessar o relatório desta reunião"

			context={
				'modal_title': modal_title,
				'modal_message': modal_message,
			}

			return render(request, "base/base_message.html", context)

	except json.JSONDecodeError:
		return JsonResponse({'error': 'Requisição JSON inválida.'}, status=400)
	except Exception as e:
		return JsonResponse({'error': str(e)}, status=500)


@login_required
def logout_confirm_modal_view(request):
	try:
		if request.method=="POST":
			data=json.loads(request.body)

			modal_title = data.get('title', 'Atenção!')
			modal_message = data.get('message', 'Confirma esta ação?')
			modal_confirm_url = data.get('confirm_url', '#')
			modal_confirm_text = data.get('confirm_text', 'Confirmar')

			modal_title="atenção! fechando sistema"
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
