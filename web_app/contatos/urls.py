from django.urls import path
from . import views


urlpatterns = [
	path("", views.index_view, name="index"),
	path("membros/", views.membro_view, name="membro_page"),
	path("parceiros/", views.parceiro_view, name="parceiro_page"),
	path("reunioes/", views.reuniao_view, name="reuniao_page"),
	path('membros/<str:pk>/', views.generic_detail_view, {'entity_type': 'membro'}, name='membro_detail'),
	path('parceiros/<str:pk>/', views.generic_detail_view, {'entity_type': 'parceiro'}, name='parceiro_detail'),
	path('reunioes/<str:pk>/', views.generic_detail_view, {'entity_type': 'reuniao'}, name='reuniao_detail'),
	path('membros/<str:pk>/editar/', views.generic_edit_view, {'entity_type': 'membro'}, name='membro_edit'),
	path('parceiros/<str:pk>/editar/', views.generic_edit_view, {'entity_type': 'parceiro'}, name='parceiro_edit'),
	path('reunioes/<str:pk>/editar/', views.generic_edit_view, {'entity_type': 'reuniao'}, name='reuniao_edit'),
	path('membros/novo/', views.generic_create_view, {'entity_type': 'membro'}, name='membro_create'),
	path('parceiros/novo/', views.generic_create_view, {'entity_type': 'parceiro'}, name='parceiro_create'),
	path('reunioes/nova/', views.generic_create_view, {'entity_type': 'reuniao'}, name='reuniao_create'),
	path('confirmar/', views.generic_alter_modal_view, name='generic_alter_modal'),
	path("login/", views.membro_login_view, name="login"),
	path("logout/confirm/", views.logout_confirm_modal_view, name="logout_confirm"),
	path("logout/", views.membro_logout_view, name="logout"),
	path("reunioes/<str:pk>/relatorio/aviso", views.warning_relatorio_modal_view, name="warning_relatorio"),
	path("hello/", views.hello_world, name="hello-world")
]
